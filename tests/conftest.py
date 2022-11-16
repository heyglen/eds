import pytest
from eds import RelativeCost, Session


@pytest.fixture
async def eds():
    async with Session() as session:
        yield session


@pytest.fixture
def relative_costs():
    return (
        RelativeCost.cheap,
        RelativeCost.mid_priced,
        RelativeCost.expensive,
    )
