import pytest 
from langserve import RemoteRunnable

@pytest.mark.parametrize(
    "first_value, expected_output",
    [
        ("How many people are in SDS_DataModel.Person?", [[8]])
    ]

)

def test_calculate_difference(first_value, expected_output):
    joke_chain = RemoteRunnable("http://dbchain:12344/simple/")
    calculation, query = joke_chain.invoke(first_value)
    print(calculation)
    assert calculation == expected_output
