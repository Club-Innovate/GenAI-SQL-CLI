USE [UtilityDB]
GO

/****** Object:  StoredProcedure [dbo].[sp_GenerateSchemaJSON]    Script Date: 3/10/2021 6:10:36 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[sp_GenerateSchemaJSON]
    @DatabaseName NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    -- Validate if the database exists
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = @DatabaseName)
    BEGIN
        PRINT 'Database does not exist.';
        RETURN;
    END

    -- Dynamic SQL to switch to the specified database
    DECLARE @sql NVARCHAR(MAX);
    SET @sql = '
    USE [' + @DatabaseName + '];

    -- Common Table Expressions (CTEs) for table and column metadata
    WITH TableData AS (
        SELECT 
            TABLE_NAME AS TableName,
            COLUMN_NAME AS ColumnName
        FROM INFORMATION_SCHEMA.COLUMNS
    ),
    Relationships AS (
        SELECT 
            FK.TABLE_NAME AS FK_Table,
            CU.COLUMN_NAME AS FK_Column,
            PK.TABLE_NAME AS PK_Table,
            PT.COLUMN_NAME AS PK_Column,
            C.CONSTRAINT_NAME AS ConstraintName
        FROM 
            INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS C
        JOIN 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS FK
        ON 
            C.CONSTRAINT_NAME = FK.CONSTRAINT_NAME
        JOIN 
            INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS PK
        ON 
            C.UNIQUE_CONSTRAINT_NAME = PK.CONSTRAINT_NAME
        JOIN 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS CU
        ON 
            C.CONSTRAINT_NAME = CU.CONSTRAINT_NAME
        JOIN 
            (
                SELECT 
                    i1.TABLE_NAME,
                    i2.COLUMN_NAME
                FROM 
                    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS i1
                JOIN 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS i2
                ON 
                    i1.CONSTRAINT_NAME = i2.CONSTRAINT_NAME
                WHERE 
                    i1.CONSTRAINT_TYPE = ''PRIMARY KEY''
            ) AS PT
        ON 
            PT.TABLE_NAME = PK.TABLE_NAME
    ),
    -- Combine table, column, and relationship data into a single dataset for JSON generation
    FormattedData AS (
        SELECT 
            T.TableName,
            (
                SELECT 
                    C.ColumnName
                FROM TableData AS C
                WHERE C.TableName = T.TableName
                FOR JSON PATH
            ) AS Columns,
            (
                SELECT 
                    R.FK_Table AS RelatedTable,
                    R.FK_Column AS ForeignKeyColumn,
                    R.PK_Table AS PrimaryTable,
                    R.PK_Column AS PrimaryKeyColumn
                FROM Relationships AS R
                WHERE R.FK_Table = T.TableName
                FOR JSON PATH
            ) AS Relationships
        FROM 
            (SELECT DISTINCT TableName FROM TableData) AS T
    )
    -- Output the final JSON schema
    SELECT 
        (
            SELECT 
                TableName,
                JSON_QUERY(Columns) AS Columns,
                JSON_QUERY(Relationships) AS Relationships
            FROM FormattedData
            FOR JSON PATH, ROOT(''Schema'')
        ) AS SchemaJson;
    ';

    -- Execute the dynamic SQL
    EXEC sp_executesql @sql;
END
GO


