from pytest import raises

from peepingtom.datablocks.datablock import DataBlock


def test_datablock():
    db = DataBlock()

    with raises(ValueError):
        db.depict()
