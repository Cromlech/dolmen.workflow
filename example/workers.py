# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.forms.crud.utils import queryClassMultiAdapter
from dolmen.workflow import IWorkflowState, IValidator

from martian.util import isclass
from zope.component import queryMultiAdapter
from zope.interface import Interface, Attribute
from zope.schema import Object
from zope.schema.fieldproperty import FieldProperty

WORKER = u'worker'


class IWorker(Interface):
    """A worklist worker.
    """
    context = Attribute('The stateful item')
    request = Attribute('The browser request')

    state = Object(
        title=u"The workflow state",
        required=True,
        schema=IWorkflowState)

    validator = Object(
        title=u"The rendered state validator",
        required=True,
        schema=IValidator)

    def update(self):
        """Called before the `render` method, this method allows to
        prepare the worker for the rendering process.
        """

    def render(self):
        """Render the worker.
        """


class BaseWorker(grok.MultiAdapter):
    grok.name(WORKER)
    grok.provides(IWorker)
    grok.baseclass()

    state = FieldProperty(IWorker['state'])
    validator = FieldProperty(IWorker['validator'])

    @property
    def template(self):
        raise NotImplementedError('You have to provide your own template')

    def update(self):
        pass

    def __init__(self, validator, state, context, request):
        self.state = state
        self.validator = validator
        self.context = context
        self.request = request

    def namespace(self):
        return {}

    def default_namespace(self):
        namespace = {}
        namespace['state'] = self.state
        namespace['request'] = self.request
        namespace['context'] = self.context
        namespace['validator'] = self.validator
        namespace['worker'] = self
        return namespace

    def render(self):
        return self.template.render(self)


def query_validator_view(item, state, validator, request):
    if isclass(validator):
        return queryClassMultiAdapter(
            (validator, state, item, request), validator, IWorker, name=WORKER)
    return queryMultiAdapter((
        validator, state, item, request), IWorker, name=WORKER)


def workers(item, state, request, validators):
    for validator in validators:
        if validator.validate(item):
            view = query_validator_view(item, state, validator, request)
            if view is not None:
                view.update()
                yield view
