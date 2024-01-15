Include (%occInclude)

Class IRISConfig.Installer Extends IRISConfig.InstallerBase
{

/// Description
ClassMethod LoadDataModelTables() As %Status
{
    Set tSC = $$$OK
    Try{
        set installDir=$System.Util.GetEnviron("TV_INSTALL_FILES")
        set dataDir=installDir_"/data"
        /*
        set className = "Person"
        set fileName = dataDir _ className _ ".csv"
        // iterate through all the files in data directory and load each one into associated table on build
        set sqlStatement = "LOAD DATA FROM FILE '" _fileName_ "' INTO SDS_DataModel." _ className
        set stmt = ##class(%SQL.Statement).%New()
        set sc = stmt.%Prepare(sqlStatement)
        //$$$ThrowStatusExceptionIfError(sc, "SQLQuickLoadSQLPrepareException")
        set rs = stmt.%Execute()
        //$$$ThrowSQLExceptionIfResultError(rs, "LOAD DATA Error: Unable to execute LOAD DATA query: "_rs.%Message)
        */
		set dir = ##class(%File).NormalizeDirectory(dataDir)
		set file=$ZSEARCH(dir_"*")
		while file'="" {
			set fileName = $PIECE(file, "/", *)
            set className = $PIECE(fileName, ".", *-1)
            
            #; if className = "Person"{
            #;     set sqlStatement = "LOAD DATA FROM FILE '" _dataDir _"/" _fileName _"' INTO SDS_DataModel." _className_ " ' (FirstName,LastName,Email,Networth) VALUES (FirstName,LastName,Email,Networth)'"
            #; }
            #; if className = "Persons"{
            #;     set sqlStatement = "LOAD DATA FROM FILE '" _dataDir _"/" _fileName _"' INTO SDS_DataModel." _className_ " ' (GreendaleID,FirstName) VALUES (GreendaleID,FirstName)'"
            #; }
            set sqlStatement = "LOAD DATA FROM FILE '" _dataDir _"/" _fileName _"' INTO SDS_DataModel." _className 
            set stmt = ##class(%SQL.Statement).%New()
            set sc = stmt.%Prepare(sqlStatement)
            $$$ThrowOnError(sc)
            set rs = stmt.%Execute()
			set file=$ZSEARCH("")
		}

    }
    Catch (oException){
        
        Set tSC = oException.AsStatus()
    }
    Quit tSC
}
/// You can customize this to run code during docker build
XData Install [ XMLNamespace = INSTALLER ]
{
<Manifest>
	
	<Namespace Name="${Namespace}" Create="no">
		<IfDef Var="SourceDir">
            <Log Text="SourceDir defined - offline install from ${SourceDir}" Level="0"/>
            <Import File="${SourceDir}" Recurse="true"/>
        </IfDef>

	</Namespace>
    <Log Text="Loading source code in the SDS namespace..." Level="0"/>
	<Namespace Name="SDS" Create="no">
        <Log Text="Populating DataModel Tables" Level="0"/>
        <Invoke Class="IRISConfig.Installer" Method="LoadDataModelTables" CheckStatus="true">
        </Invoke>
    </Namespace>
		
</Manifest>
}

}
