Class src.Person Extends (%Persistent, %Populate)
{

Property FirstName As %String [ Required ];

Property LastName As %String [ Required ];

//Property DOB As %Date(FORMAT = 5, MAXVAL = "+$h");

Property Email As %String [ Required ];

Property NetWorth As %Integer [Required]; 
}
