from typing import Optional, cast

from eventsourcing.domain.model.decorators import attribute
from eventsourcing.domain.model.entity import (
    EntityWithHashchain,
    TimestampedVersionedEntity,
)
from eventsourcing.types import AbstractEntityRepository, T


class Example(EntityWithHashchain[T], TimestampedVersionedEntity[T]):
    """
    An example event sourced domain model entity.
    """

    class Event(EntityWithHashchain.Event[T], TimestampedVersionedEntity.Event[T]):
        """Supertype for events of example entities."""

    class Created(
        Event, EntityWithHashchain.Created[T], TimestampedVersionedEntity.Created[T]
    ):
        """Published when an Example is created."""

    class AttributeChanged(Event[T], TimestampedVersionedEntity.AttributeChanged[T]):
        """Published when an Example is created."""

    class Discarded(Event[T], TimestampedVersionedEntity.Discarded[T]):
        """Published when an Example is discarded."""

    class Heartbeat(Event[T], TimestampedVersionedEntity.Event[T]):
        """Published when a heartbeat in the entity occurs (see below)."""

        def mutate(self, obj: Optional[T]) -> None:
            """Updates 'obj' with values from self."""
            obj = cast(Example, obj)
            obj._count_heartbeats += 1

    def __init__(self, foo="", a="", b="", **kwargs):
        super(Example, self).__init__(**kwargs)
        self._foo = foo
        self._a = a
        self._b = b
        self._count_heartbeats = 0

    @attribute
    def foo(self):
        """An example attribute."""

    @attribute
    def a(self):
        """An example attribute."""

    @attribute
    def b(self):
        """Another example attribute."""

    def beat_heart(self, number_of_beats=1):
        self.__assert_not_discarded__()
        while number_of_beats > 0:
            self.__trigger_event__(self.Heartbeat)
            number_of_beats -= 1

    def count_heartbeats(self):
        return self._count_heartbeats


class AbstractExampleRepository(AbstractEntityRepository):
    pass


def create_new_example(foo="", a="", b=""):
    """
    Factory method for example entities.

    :rtype: Example
    """
    return Example.__create__(foo=foo, a=a, b=b)
