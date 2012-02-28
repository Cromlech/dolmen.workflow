# -*- coding: utf-8 -*-

from dolmen.workflow import IValidator, Error
from some_hypothetical_package import IDocument, IDocumentsContainer
from zope.interface import moduleProvides, classProvides, Invalid
from zope.interface.verify import verifyObject


class DocumentValidator(object):
    classProvides(IValidator)

    title = _(u"No uploaded documents")
    identifier = u"task.validator.document"
    error = Error(identifier=identifier, title=title)

    @classmethod
    def validate(cls, obj):
        try:
            container = IDocumentsContainer(obj, None)
            if container is not None and len(container):
                return None
        except Invalid:
            pass
        return cls.error
