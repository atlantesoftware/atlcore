# -*- coding: utf-8 -*-
import datetime
import re

from dateutil import rrule

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.template.defaultfilters import date
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext, ugettext_lazy as _

from atlcore.schedule.utils import EventListManager, OccurrenceReplacer
from atlcore.contenttype.models import Content, Container

from atlcore.libs.stdimage import StdImageField

class BaseCalendar(Container):
    '''
    '''
    
    slug = models.SlugField(_("slug"),max_length = 200)
    image = StdImageField(upload_to='images/calendars', blank=True, size=(640, 480), thumbnail_size=(100, 100, True))
    objects = models.Manager()

    class Meta:
        abstract = True
        
    @property
    def name(self):
        return self.title

    def events(self):
        return self.children.all()
    events = property(events)

    def get_recent(self, amount=5, in_datetime = datetime.datetime.now):
        """
        """
        return self.events.order_by('-start_date', '-start_time').filter(start_date__lt=datetime.date.today())[:amount]

    def occurrences_after(self, date=None):
        return EventListManager(self.events.all()).occurrences_after(date)

    def get_absolute_url(self):
        return reverse('calendar_home', kwargs={'calendar_slug':self.slug})

    def add_event_url(self):
        return reverse('s_create_event_in_calendar', args=[self.slug])
    
class Calendar(BaseCalendar):
    
    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendar')    

freqs = (   
    ("YEARLY", _("Yearly")),
    ("MONTHLY", _("Monthly")),
    ("WEEKLY", _("Weekly")),
    ("DAILY", _("Daily")),
#    ("HOURLY", _("Hourly")),
#    ("MINUTELY", _("Minutely")),
#    ("SECONDLY", _("Secondly")),
)

week_days = ('MO','TU','WE','TH','FR','SA','SO')


class BaseEvent(Content):
    '''
    This model stores meta data for a date.  You can relate this data to many
    other models.
    '''
    #start = models.CharField(_("start date"), max_length = 255, help_text=_("Please enter the date in the format DD/MM/YYYY."))
    start_date = models.DateField(_("start date"), default=datetime.datetime.now().date())
    start_time = models.TimeField(_("start time"), default=datetime.datetime.now().time())
    end_date = models.DateField(_("end date"), default=datetime.datetime.now(), max_length = 255, null = True, blank = True, help_text=_("Please enter the end date of the event.")) 
    end_time = models.TimeField(_("end time"), default=(datetime.datetime.now() + datetime.timedelta(minutes=30)).time(), help_text=_("The end time must be later than the start time."))
    full_day = models.BooleanField(_('full day'), default=False)
    end_recurring_period = models.DateTimeField(_("end recurring period"), null = True, blank = True, help_text=_("This date is ignored for one time only events."))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10, blank = True)
    image = StdImageField(upload_to='images/events', blank=True, thumbnail_size=(100, 100, True))
    params = models.TextField(_("params"), null=True, blank=True)
       
    objects = models.Manager()

    class Meta:
        abstract = True
        
    def start_datetime(self):
        return datetime.datetime.combine(self.start_date, self.start_time)
    
    def end_datetime(self):
        return datetime.datetime.combine(self.start_date, self.end_time)         

    def __unicode__(self):
        date_format = u'l, %s' % ugettext("DATE_FORMAT")
        return ugettext('%(title)s %(start_date)s') % {
            'title': self.title,
            'start_date': date(self.start_date, date_format)
        }
        
    def __get_date_from_params__(self, prefix):
        if self.params:
            l = re.findall('%s\d{1,2}/\d{1,2}/\d{4}'%prefix, self.params)
            if l:
                d = l[0][len(prefix):]
                args = d.split('/')
                try:
                    y = int(args[2])
                    m = int(args[1])
                    d = int(args[0])                   
                    return datetime.datetime(y,m,d)
                except:
                    pass
        return None
    
    def save(self):
        super(BaseEvent,self).save()
        need_to_save = False
        sd = self.__get_date_from_params__('dtstart:date')
        if sd is not None and sd != self.start_date:
            self.start_date = sd
            need_to_save = True
        ed = self.__get_date_from_params__('until:date')
        if ed is not None and ed != self.end_recurring_period:
            self.end_recurring_period = ed
            need_to_save = True
        if need_to_save:
            self.save()

    def get_absolute_url(self):
        instance = self.get_instance()
        info=instance._meta.module_name
        if (info == 'link' or info == 'banner'):
            return instance.url
        else:
            return reverse('%s_details' % info, args=[self.id, self.slug])       

    def get_occurrences(self, start, end):
        """
        """
        persisted_occurrences = self.occurrence_set.all()
        occ_replacer = OccurrenceReplacer(persisted_occurrences)
        occurrences = self._get_occurrence_list(start, end)
        final_occurrences = []
        for occ in occurrences:
            # replace occurrences with their persisted counterparts
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)
                # ...but only if they are within this period
                if p_occ.start < end and p_occ.end >= start:
                    final_occurrences.append(p_occ)
            else:
                final_occurrences.append(occ)
        # then add persisted occurrences which originated outside of this period but now
        # fall within it
        final_occurrences += occ_replacer.get_additional_occurrences(start, end)
        return final_occurrences
    
    def get_params(self):
        """
        """
        if self.params is None:
            return {}
        params = self.params.split(';')
        param_dict = []
        for param in params:
            param = param.split(':')
            err = False
            if len(param) == 2:
                cmd = str(param[0]).strip()
                arg = str(param[1]).strip()
                if arg[:4] == 'date':
                    args = arg[4:].split('/')
                    try:
                        y = int(args[2])
                        m = int(args[1])
                        d = int(args[0])  
                        if cmd == 'dtstart':
                            time = self.start_time
                        else:
                            time = self.end_time                 
                        arg = datetime.datetime.combine(datetime.datetime(y,m,d), time)
                    except:
                        err = True
                elif arg[:2] == '(+' and arg[-1:] == ')':
                    try:
                        wd = self.start_date.weekday()
                        arg = eval('rrule.%s' %(week_days[wd] + arg))
                    except:
                        err = True
                elif arg.find(',') != -1:
                    arg = [int(p) for p in arg.split(',')]
                else:
                    arg = int(arg)
                if not err:              
                    param = (cmd, arg)
                    param_dict.append(param)
        return dict(param_dict)    

    def get_rrule_object(self):
        if self.frequency:
            params = self.get_params()
            frequency = 'rrule.%s' % self.frequency
            return rrule.rrule(eval(frequency), **params)

    def _create_occurrence(self, start, end=None):
        """Las subclases tienen que implentar este método"""
        raise NotImplementedError

    def get_occurrence(self, date):
        """Las subclases tienen que implentar este método"""
        raise NotImplementedError

    def _get_occurrence_list(self, start, end):
        """
        returns a list of occurrences for this event from start to end.
        """
        event_end = datetime.datetime.combine(self.start_date, self.end_time)
        event_start = datetime.datetime.combine(self.start_date, self.start_time)
        difference = event_end - event_start
        if self.frequency:
            occurrences = []
            if self.end_recurring_period and self.end_recurring_period < end:
                end = self.end_recurring_period
            rule = self.get_rrule_object()
            o_starts = rule.between(start-difference, end, inc=True)
            for o_start in o_starts:
                o_end = o_start + difference
                occurrences.append(self._create_occurrence(o_start, o_end))
            return occurrences
        else:
            # check if event is in the period
            if event_start < end and event_end >= start:
                return [self._create_occurrence(event_start)]
            else:
                return []

    def _occurrences_after_generator(self, after=None):
        """
        returns a generator that produces unpresisted occurrences after the
        datetime ``after``.
        """
        event_end = datetime.datetime.combine(self.start_date, self.end_time)
        event_start = datetime.datetime.combine(self.start_date, self.start_time)
        if after is None:
            after = datetime.datetime.now()
        rule = self.get_rrule_object()
        if rule is None:
            if event_end > after:
                yield self._create_occurrence(event_start, event_end)
            raise StopIteration
        date_iter = iter(rule)
        difference = event_end - event_start
        while True:
            o_start = date_iter.next()
            if o_start > self.end_recurring_period:
                raise StopIteration
            o_end = o_start + difference
            if o_end > after:
                yield self._create_occurrence(o_start, o_end)


    def occurrences_after(self, after=None):
        """
        returns a generator that produces occurrences after the datetime
        ``after``.  Includes all of the persisted Occurrences.
        """
        occ_replacer = OccurrenceReplacer(self.occurrence_set.all())
        generator = self._occurrences_after_generator(after)
        while True:
            next = generator.next()
            yield occ_replacer.get_occurrence(next)


class Event(BaseEvent):
    
    PARENT_TYPES = ['schedule.calendar']
    
    @property
    def calendar(self):
        return self.parent
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        
    def _create_occurrence(self, start, end=None):
        if end is None:
            end = start + (datetime.datetime.combine(self.start_date, self.end_time) - datetime.datetime.combine(self.start_date, self.start_time))
        return Occurrence(event=self,start=start,end=end, original_start=start, original_end=end)

    def get_occurrence(self, date):
        rule = self.get_rrule_object()
        if rule:
            next_occurrence = rule.after(date, inc=True)
        else:
            next_occurrence = datetime.datetime.combine(self.start_date, self.start_time)
        if next_occurrence == date:
            try:
                return Occurrence.objects.get(event = self, original_start = date)
            except Occurrence.DoesNotExist:
                return self._create_occurrence(next_occurrence)          


class BaseOccurrence(models.Model):
    
    title = models.CharField(_("title"), max_length=255, blank=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"))
    cancelled = models.BooleanField(_("cancelled"), default=False)
    original_start = models.DateTimeField(_("original start"))
    original_end = models.DateTimeField(_("original end"))

    class Meta:
        abstract = True
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")
        

    def __init__(self, *args, **kwargs):
        super(BaseOccurrence, self).__init__(*args, **kwargs)
        if self.title is None:
            self.title = self.event.title
        if self.description is None:
            self.description = self.event.description


    def moved(self):
        return self.original_start != self.start or self.original_end != self.end
    moved = property(moved)

    def move(self, new_start, new_end):
        self.start = new_start
        self.end = new_end
        self.save()

    def cancel(self):
        self.cancelled = True
        self.save()

    def uncancel(self):
        self.cancelled = False
        self.save()

    def get_absolute_url(self):
        if self.pk is not None:
            return reverse('occurrence', kwargs={'occurrence_id': self.pk, 'event_id': self.event.id})
        return reverse('occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def get_cancel_url(self):
        if self.pk is not None:
            return reverse('cancel_occurrence', kwargs={'occurrence_id': self.pk, 'event_id': self.event.id})
        return reverse('cancel_occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def get_edit_url(self):
        if self.pk is not None:
            return reverse('edit_occurrence', kwargs={'occurrence_id': self.pk, 'event_id': self.event.id})
        return reverse('edit_occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def __unicode__(self):
        return ugettext("%(start)s to %(end)s") % {
            'start': self.start,
            'end': self.end,
        }

    def __cmp__(self, other):
        rank = cmp(self.start, other.start)
        if rank == 0:
            return cmp(self.end, other.end)
        return rank

    def __eq__(self, other):
        return self.event == other.event and self.original_start == other.original_start and self.original_end == other.original_end

class Occurrence(BaseOccurrence):
    
    event = models.ForeignKey(Event, verbose_name=_("event"))  


def optionnal_calendar(sender, **kwargs):
    event = kwargs.pop('instance')

    if not isinstance(event, Event):
        return True
    if not event.calendar:
        try:
            calendar = Calendar._default_manager.get(title='default')
        except Calendar.DoesNotExist:
            calendar = Calendar(title='default', slug='default')
            calendar.save()

        event.parent = calendar
    return True

pre_save.connect(optionnal_calendar)
