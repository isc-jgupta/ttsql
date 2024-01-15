import pytest 
#from py.xml import html
from langserve import RemoteRunnable

@pytest.mark.parametrize(
    "first_value, expected_output",
    [
        ("Number of people in SDS_DataModel.Person?", [[8]]),
        ("List all emails from SDS_DataModel.Person", [['Jeff'],['Britta'],['Abed'],['Annie'],['Troy'],['Pierce'],['Shirley'],['Craig']]),
        ("List the FirstName with the largest NetWorth SDS_DataModel.Person", [['Hawthorne'],['Barnes'],['Winger'],['Pelton'],['Bennett'],['Perry'],['Edison'],['Nadir']]),
        ("Is there someone with the FirstName Jack in SDS_DataModel.Person", [[0]]),
        ("How many tables contain a column with NetWorth", [[0]]),
        ("How many people have a OnCampusJob as a Trainer in SDS_DataModel.Campus", [[1]]),
        ("How many GreendaleID are 'True' in SDS_DataModel.Campus", [[2]]),
    ]

)

def test_calculate_difference(first_value, expected_output):
    joke_chain = RemoteRunnable("http://dbchain:12344/simple/")
    calculation, query= joke_chain.invoke(first_value)
    assert calculation == expected_output

def pytest_html_report_title(report):
   report.title = "Results of Test2!"
