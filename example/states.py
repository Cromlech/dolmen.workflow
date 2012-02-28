# -*- coding: utf-8 -*-

import validators
from interfaces import IStateComponent
from dolmen.workflow import States, Validators
from dolmen.workflow.components import check_validators
from zope.interface import moduleProvides, classProvides


class State(object):
    """A class-level state.
    """
    pre_validators = Validators()
    post_validators = Validators()
    states = States()
    description = u""

    @classmethod
    def __repr__(cls):
        return u"<State %r>" % cls.identifier

    @classmethod
    def clone(self, new_identifier=None):
        raise NotImplementedError("States can't be cloned")

    @classmethod
    def check_constraints(cls, item, raiseErrors=False):
        return check_validators(item, cls.pre_validators)

    @classmethod
    def check_locks(cls, item, raiseErrors=False):
        return check_validators(item, cls.post_validators)

    @classmethod
    def get_reachable_states(cls, item):
        if bool(cls.check_locks(item)) is False:
            return dict([(state.action or state.title, state)
                         for state in cls.states
                         if not state.check_constraints(item)])
        return {}


class Cancelled(State):
    classProvides(IStateComponent)

    title = _(u"Cancelled")
    identifier = "myproject.cancelled"
    action = _(u"Cancel")


class Finished(State):
    classProvides(IStateComponent)

    title = _(u"Finished")
    identifier = "myproject.final.finished"
    action = _(u"Mark as finished")


class Sent(State):
    classProvides(IStateComponent)

    title = _(u"Sent")
    identifier = "myproject.final.sent"
    action = _(u"Mark as sent")

    states = States(Finished)


class Delivered(States):
    classProvides(IStateComponent)

    title = _(u"Delivered")
    identifier = "myproject.final.delivered"
    action = _(u"Mark as delivered")

    states = States(Sent)


class DirectSent(State):
    classProvides(IStateComponent)

    identifier = "myproject.publisher.direct_sent"
    action = _(u"Mark as sent directly")
    title = _(u"Sent directly")
    states = States(Finished)


class ReadyForDirectSend(State):
    classProvides(IStateComponent)

    title = _(u"Ready for direct delivery")
    identifier = "myproject.publisher.ready_for_direct_send"
    action = _(u"Mark as ready for direct delivery")

    states = States(DirectSent)


class ReadyForDelivery(State):
    classProvides(IStateComponent)

    title = _(u"Ready for delivery")
    identifier = "myproject.final.ready_for_delivery"
    action = _(u"Mark as ready for delivery")

    states = States(Delivered)


class Processing(State):
    classProvides(IStateComponent)

    title = _(u"Processing")
    identifier = "myproject.publisher.processing"
    action = _(u"Start processing")

    states = States(ReadyForDelivery, ReadyForDirectSend)


class WaitingForTreatment(State):
    classProvides(IStateComponent)

    title = _(u"Waiting for treatment")
    identifier = "myproject.publisher.pending"
    action = _(u"Submit to treatment")

    # We make sure we cannot arrive in this state with a broken task.
    pre_validators = Validators(
        validators.DocumentValidator)

    # We make sure we cannot get out of this state with a broken task.
    post_validators = Validators(
        validators.DocumentValidator)


class WaitingForCompletion(State):
    classProvides(IStateComponent)

    title = _(u"Waiting for completion")
    identifier = "myproject.client.pending"
    action = _(u"Wait for complement")

    states = States(WaitingForTreatment, Cancelled)


# Deferred assignation
WaitingForTreatment.states = States(
    Processing, WaitingForCompletion, Cancelled)
