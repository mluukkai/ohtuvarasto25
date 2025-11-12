*** Settings ***
Documentation     Comprehensive E2E tests for Varasto web application
Library           SeleniumLibrary
Suite Setup       Open Browser And Go To Home
Suite Teardown    Close Browser
Test Setup        Go To Home Page

*** Variables ***
${SERVER_URL}     http://127.0.0.1:5000
${BROWSER}        headlesschrome
${DELAY}          0

*** Test Cases ***
Application Starts And Shows Empty State
    [Documentation]    Verify that the application starts correctly with no warehouses
    Go To    ${SERVER_URL}
    Page Should Contain    Varastonhallintajärjestelmä
    Page Should Contain    Ei varastoja. Luo ensimmäinen varastosi!
    Page Should Contain Element    xpath://a[contains(@href, '/new')]

Navigate To Create Warehouse Page
    [Documentation]    Verify navigation to warehouse creation page
    Go To    ${SERVER_URL}
    Click Link    xpath://a[contains(@href, '/new')]
    Location Should Be    ${SERVER_URL}/new
    Page Should Contain    Luo uusi varasto
    Page Should Contain Element    name:name
    Page Should Contain Element    name:tilavuus
    Page Should Contain Element    name:alku_saldo

Create Single Warehouse Successfully
    [Documentation]    Create a warehouse and verify it appears in the list
    Create Warehouse    Testivarasto    100    50
    Page Should Contain    Testivarasto
    Page Should Contain    Saldo:
    Page Should Contain    50.00
    Page Should Contain    Tilavuus:
    Page Should Contain    100.00
    Page Should Contain    Vapaana:
    Page Should Contain    50.00

Create Multiple Warehouses
    [Documentation]    Create multiple warehouses and verify all are displayed
    Create Warehouse    Mehuvarasto    100    20
    Create Warehouse    Olutvarasto    150    75
    Create Warehouse    Maitovarasto    200    50
    Page Should Contain    Varastot (3)
    Page Should Contain    Mehuvarasto
    Page Should Contain    Olutvarasto
    Page Should Contain    Maitovarasto

Create Warehouse With Zero Initial Balance
    [Documentation]    Verify warehouse can be created with zero initial balance
    Create Warehouse    Tyhjä varasto    100    0
    Page Should Contain    Tyhjä varasto
    Page Should Contain    Saldo:
    Element Should Contain    xpath://div[contains(., 'Tyhjä varasto')]//following::span[contains(., 'Saldo:')]/following-sibling::span    0.00

Create Warehouse Validation - Empty Name
    [Documentation]    Verify validation for empty warehouse name
    Go To    ${SERVER_URL}/new
    Input Text    name:tilavuus    100
    Input Text    name:alku_saldo    0
    Click Button    Luo varasto
    Page Should Contain    Nimi on pakollinen!

Create Warehouse Validation - Zero Capacity
    [Documentation]    Verify validation for zero capacity
    Go To    ${SERVER_URL}/new
    Input Text    name:name    Testivarasto
    Input Text    name:tilavuus    0
    Input Text    name:alku_saldo    0
    Click Button    Luo varasto
    Page Should Contain    Tilavuuden pitää olla suurempi kuin 0!

Create Warehouse Validation - Negative Capacity
    [Documentation]    Verify validation for negative capacity
    Go To    ${SERVER_URL}/new
    Input Text    name:name    Testivarasto
    Input Text    name:tilavuus    -50
    Input Text    name:alku_saldo    0
    Click Button    Luo varasto
    Page Should Contain    Tilavuuden pitää olla suurempi kuin 0!

Add Items To Warehouse
    [Documentation]    Add items to warehouse and verify balance updates
    Create Warehouse    Testivarasto    100    20
    ${first_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${first_saldo}    20.00
    Add Items To Warehouse    Testivarasto    30
    ${second_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${second_saldo}    50.00

Add Items Until Full
    [Documentation]    Add items until warehouse is full
    Create Warehouse    Testivarasto    100    90
    Add Items To Warehouse    Testivarasto    20
    ${final_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${final_saldo}    100.00

Remove Items From Warehouse
    [Documentation]    Remove items from warehouse and verify balance updates
    Create Warehouse    Testivarasto    100    50
    Remove Items From Warehouse    Testivarasto    20
    ${new_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${new_saldo}    30.00

Remove All Items From Warehouse
    [Documentation]    Remove all items from warehouse
    Create Warehouse    Testivarasto    100    50
    Remove Items From Warehouse    Testivarasto    50
    ${final_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${final_saldo}    0.00

Remove More Items Than Available
    [Documentation]    Try to remove more items than available - should take all
    Create Warehouse    Testivarasto    100    30
    Remove Items From Warehouse    Testivarasto    50
    ${final_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${final_saldo}    0.00

Delete Warehouse
    [Documentation]    Delete a warehouse and verify it's removed
    Create Warehouse    Testivarasto    100    50
    Page Should Contain    Testivarasto
    Delete Warehouse    Testivarasto
    Page Should Not Contain    Testivarasto
    Page Should Contain    poistettu!

Delete Warehouse With Confirmation
    [Documentation]    Verify delete confirmation dialog
    Create Warehouse    Testivarasto    100    50
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., 'Testivarasto')]//ancestor::div[contains(@class, 'warehouse-card')]//button[contains(text(), 'Poista varasto')]
    # Note: In headless mode, confirm dialog is automatically accepted
    Click Button    ${warehouse_xpath}
    Page Should Not Contain    Testivarasto

Multiple Operations On Same Warehouse
    [Documentation]    Perform multiple operations on the same warehouse
    Create Warehouse    Testivarasto    100    20
    Add Items To Warehouse    Testivarasto    30
    ${saldo1}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${saldo1}    50.00
    Remove Items From Warehouse    Testivarasto    10
    ${saldo2}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${saldo2}    40.00
    Add Items To Warehouse    Testivarasto    15
    ${saldo3}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${saldo3}    55.00

Multiple Warehouses Independent Operations
    [Documentation]    Verify operations on one warehouse don't affect others
    Create Warehouse    Varasto1    100    30
    Create Warehouse    Varasto2    200    50
    Add Items To Warehouse    Varasto1    20
    ${saldo1}=    Get Warehouse Balance    Varasto1
    ${saldo2}=    Get Warehouse Balance    Varasto2
    Should Be Equal As Numbers    ${saldo1}    50.00
    Should Be Equal As Numbers    ${saldo2}    50.00

Progress Bar Shows Correct Percentage
    [Documentation]    Verify progress bar displays correct fill percentage
    Create Warehouse    Testivarasto    100    50
    ${progress}=    Get Warehouse Progress Percentage    Testivarasto
    Should Be Equal As Strings    ${progress}    50%

Free Space Calculation
    [Documentation]    Verify free space is calculated correctly
    Create Warehouse    Testivarasto    100    30
    ${free_space}=    Get Warehouse Free Space    Testivarasto
    Should Be Equal As Numbers    ${free_space}    70.00

Back Button From Create Page
    [Documentation]    Verify back button works from create page
    Go To    ${SERVER_URL}/new
    Click Button    Takaisin
    Location Should Be    ${SERVER_URL}/
    Page Should Contain    Varastonhallintajärjestelmä

Success Message After Creating Warehouse
    [Documentation]    Verify success message appears after creating warehouse
    Go To    ${SERVER_URL}/new
    Input Text    name:name    Testivarasto
    Input Text    name:tilavuus    100
    Input Text    name:alku_saldo    50
    Click Button    Luo varasto
    Page Should Contain    luotu onnistuneesti!

Success Message After Adding Items
    [Documentation]    Verify success message appears after adding items
    Create Warehouse    Testivarasto    100    20
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., 'Testivarasto')]//ancestor::div[contains(@class, 'warehouse-card')]
    Input Text    ${warehouse_xpath}//form[@action='/add/1']//input[@name='maara']    10
    Click Button    ${warehouse_xpath}//form[@action='/add/1']//button
    Page Should Contain    Lisätty 10

Success Message After Removing Items
    [Documentation]    Verify success message appears after removing items
    Create Warehouse    Testivarasto    100    50
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., 'Testivarasto')]//ancestor::div[contains(@class, 'warehouse-card')]
    Input Text    ${warehouse_xpath}//form[@action='/take/1']//input[@name='maara']    20
    Click Button    ${warehouse_xpath}//form[@action='/take/1']//button
    Page Should Contain    Otettu 20

Create Warehouse With Decimal Values
    [Documentation]    Verify decimal values work correctly
    Create Warehouse    Testivarasto    150.5    75.25
    Page Should Contain    Testivarasto
    ${saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${saldo}    75.25

Add Decimal Amount
    [Documentation]    Add decimal amount to warehouse
    Create Warehouse    Testivarasto    100    20
    Add Items To Warehouse    Testivarasto    15.75
    ${new_saldo}=    Get Warehouse Balance    Testivarasto
    Should Be Equal As Numbers    ${new_saldo}    35.75

Page Title Is Correct
    [Documentation]    Verify page titles are correct
    Go To    ${SERVER_URL}
    Title Should Be    Varasto - Varastonhallinta
    Go To    ${SERVER_URL}/new
    Title Should Be    Luo uusi varasto - Varastonhallinta

CSS Styling Is Applied
    [Documentation]    Verify CSS file is loaded and applied
    Go To    ${SERVER_URL}
    ${css_link}=    Get Element Attribute    xpath://link[@rel='stylesheet']    href
    Should Contain    ${css_link}    style.css

Warehouse Count Display
    [Documentation]    Verify warehouse count is displayed correctly
    Create Warehouse    Varasto1    100    50
    Page Should Contain    Varastot (1)
    Create Warehouse    Varasto2    100    50
    Page Should Contain    Varastot (2)
    Create Warehouse    Varasto3    100    50
    Page Should Contain    Varastot (3)

Create Button Visible When Warehouses Exist
    [Documentation]    Verify create button is visible even when warehouses exist
    Create Warehouse    Testivarasto    100    50
    Page Should Contain Element    xpath://a[contains(@href, '/new')]
    Element Should Be Visible    xpath://a[contains(@href, '/new')]

*** Keywords ***
Open Browser And Go To Home
    [Documentation]    Open browser and navigate to application
    Open Browser    ${SERVER_URL}    ${BROWSER}
    Set Selenium Speed    ${DELAY}
    Go To    ${SERVER_URL}

Go To Home Page
    [Documentation]    Navigate to home page (resets state since app uses in-memory storage)
    Go To    ${SERVER_URL}

Create Warehouse
    [Arguments]    ${name}    ${capacity}    ${initial_balance}
    [Documentation]    Create a new warehouse with given parameters
    Go To    ${SERVER_URL}/new
    Input Text    name:name    ${name}
    Input Text    name:tilavuus    ${capacity}
    Input Text    name:alku_saldo    ${initial_balance}
    Click Button    Luo varasto

Add Items To Warehouse
    [Arguments]    ${warehouse_name}    ${amount}
    [Documentation]    Add items to specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    ${form_xpath}=    Set Variable    ${warehouse_xpath}//form[contains(@action, '/add/')]
    Input Text    ${form_xpath}//input[@name='maara']    ${amount}
    Click Button    ${form_xpath}//button

Remove Items From Warehouse
    [Arguments]    ${warehouse_name}    ${amount}
    [Documentation]    Remove items from specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    ${form_xpath}=    Set Variable    ${warehouse_xpath}//form[contains(@action, '/take/')]
    Input Text    ${form_xpath}//input[@name='maara']    ${amount}
    Click Button    ${form_xpath}//button

Delete Warehouse
    [Arguments]    ${warehouse_name}
    [Documentation]    Delete specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    Click Button    ${warehouse_xpath}//button[contains(text(), 'Poista varasto')]

Get Warehouse Balance
    [Arguments]    ${warehouse_name}
    [Documentation]    Get current balance of specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    ${balance_xpath}=    Set Variable    ${warehouse_xpath}//span[contains(text(), 'Saldo:')]/following-sibling::span
    ${balance}=    Get Text    ${balance_xpath}
    [Return]    ${balance}

Get Warehouse Free Space
    [Arguments]    ${warehouse_name}
    [Documentation]    Get free space of specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    ${free_xpath}=    Set Variable    ${warehouse_xpath}//span[contains(text(), 'Vapaana:')]/following-sibling::span
    ${free_space}=    Get Text    ${free_xpath}
    [Return]    ${free_space}

Get Warehouse Progress Percentage
    [Arguments]    ${warehouse_name}
    [Documentation]    Get progress bar percentage of specified warehouse
    ${warehouse_xpath}=    Set Variable    xpath://div[contains(., '${warehouse_name}')]//ancestor::div[contains(@class, 'warehouse-card')]
    ${progress_xpath}=    Set Variable    ${warehouse_xpath}//div[contains(@class, 'progress-fill')]
    ${percentage}=    Get Text    ${progress_xpath}
    [Return]    ${percentage}
