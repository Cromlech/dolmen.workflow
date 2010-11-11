"""
Workflow state
==============

  >>> from dolmen.workflow import State, IWorkflowState
  >>> from zope.interface.verify import verifyClass, verifyObject

  >>> verifyClass(IWorkflowState, State)
  True

  >>> anger = State(identifier='anger', title='Anger')
  >>> verifyObject(IWorkflowState, anger)
  True

  >>> print anger.states, list(anger.states)
  <States> []

  >>> print anger.pre_validators, list(anger.pre_validators)
  <Validators> []

  >>> print anger.post_validators, list(anger.post_validators)
  <Validators> []


Validators and checkers
~~~~~~~~~~~~~~~~~~~~~~~

  >>> class MyStatefulObject(object):
  ...     pass

  >>> item = MyStatefulObject()
  >>> print anger.get_reachable_states(item)
  {}

  >>> print 'errors: %s' % anger.check_constraints(item)
  errors: []

  >>> print 'errors: %s' % anger.check_locks(item)
  errors: []


State transition
----------------

Validators
~~~~~~~~~~

  >>> from zope.interface import Interface, classProvides
  >>> from dolmen.workflow import IValidator, Validators, Error

  >>> class ICalmed(Interface):
  ...     pass

  >>> class ModelIsCalm(object):
  ...     classProvides(IValidator)
  ...
  ...     identifier = u'Calm'
  ...
  ...     error = Error(
  ...       identifier='calmer',
  ...       title='The model is not calm')
  ...
  ...     @classmethod
  ...     def validate(cls, obj):
  ...         if not ICalmed.providedBy(obj):
  ...             return cls.error
  ...         return None

  >>> calm = State(identifier='calm', title='Calm', action=u'calm down',
  ...              pre_validators=Validators(ModelIsCalm))

  >>> calm.check_constraints(item)
  [<Error The model is not calm>]


Setting up transitions
~~~~~~~~~~~~~~~~~~~~~~

  >>> anger.states.append(calm)
  >>> print anger.get_reachable_states(item)
  {}

  >>> from zope.interface import alsoProvides
  >>> alsoProvides(item, ICalmed)

  >>> print anger.get_reachable_states(item)
  {u'calm down': <State Calm>}


Understanding the locks
~~~~~~~~~~~~~~~~~~~~~~~

  >>> class ModelCanMoveOn(object):
  ...     classProvides(IValidator)
  ...
  ...     identifier = u'move on'
  ...
  ...     error = Error(
  ...       identifier='move.on',
  ...       title='The model can not move on')
  ...
  ...     @classmethod
  ...     def validate(cls, obj):
  ...         if getattr(obj, 'move', False) is True:
  ...             return None
  ...         return cls.error

  >>> anger.post_validators.append(ModelCanMoveOn)
  >>> print anger.get_reachable_states(item)
  {}

  >>> anger.check_locks(item)
  [<Error The model can not move on>]

  >>> setattr(item, 'move', True)
  >>> anger.check_locks(item)
  []

  >>> print anger.get_reachable_states(item)
  {u'calm down': <State Calm>}

"""
