# Robot Framework E2E Tests for Varasto

This directory contains comprehensive end-to-end tests for the Varasto web application using Robot Framework and SeleniumLibrary.

## Test Coverage

The test suite includes **29 test cases** covering all major user workflows:

### Application & Navigation (3 tests)
- `Application Starts And Shows Empty State` - Verify initial state
- `Navigate To Create Warehouse Page` - Test navigation flows
- `Back Button From Create Page` - Verify back navigation

### Warehouse Creation (7 tests)
- `Create Single Warehouse Successfully` - Basic creation flow
- `Create Multiple Warehouses` - Multiple warehouse support
- `Create Warehouse With Zero Initial Balance` - Edge case testing
- `Create Warehouse With Decimal Values` - Decimal number support
- `Create Warehouse Validation - Empty Name` - Name validation
- `Create Warehouse Validation - Zero Capacity` - Capacity validation
- `Create Warehouse Validation - Negative Capacity` - Negative value handling

### Warehouse Operations (10 tests)
- `Add Items To Warehouse` - Add items and verify balance
- `Add Items Until Full` - Fill warehouse to capacity
- `Add Decimal Amount` - Decimal amount operations
- `Remove Items From Warehouse` - Remove items
- `Remove All Items From Warehouse` - Empty warehouse
- `Remove More Items Than Available` - Edge case handling
- `Multiple Operations On Same Warehouse` - Sequential operations
- `Multiple Warehouses Independent Operations` - Isolation verification

### Warehouse Deletion (2 tests)
- `Delete Warehouse` - Basic deletion
- `Delete Warehouse With Confirmation` - Confirmation dialog handling

### UI Verification (7 tests)
- `Progress Bar Shows Correct Percentage` - Visual feedback
- `Free Space Calculation` - Calculation accuracy
- `Success Message After Creating Warehouse` - User feedback
- `Success Message After Adding Items` - Operation feedback
- `Success Message After Removing Items` - Operation feedback  
- `Page Title Is Correct` - Page metadata
- `CSS Styling Is Applied` - Styling verification
- `Warehouse Count Display` - Counter accuracy
- `Create Button Visible When Warehouses Exist` - UI consistency

## Running Tests

### Quick Start
```bash
# From repository root
./run_robot_tests.sh
```

### Manual Execution
```bash
# Terminal 1: Start Flask application
cd src
export FLASK_DEBUG=false
poetry run python app.py

# Terminal 2: Run tests
cd ..
poetry run robot --outputdir robot-results src/tests/robot/varasto_web.robot
```

### Viewing Results
After test execution, open these files in your browser:
- `robot-results/report.html` - High-level test execution report
- `robot-results/log.html` - Detailed test log with screenshots
- `robot-results/output.xml` - Machine-readable results

## Test Architecture

### Libraries Used
- **SeleniumLibrary** - Browser automation
- **Robot Framework** - Test framework and keywords

### Browser Configuration
- **Browser**: Headless Chrome (configurable via `${BROWSER}` variable)
- **Delay**: 0 seconds for fast execution
- **Base URL**: http://127.0.0.1:5000

### Custom Keywords
The test suite includes several custom keywords for common operations:

- `Open Browser And Go To Home` - Initialize browser session
- `Go To Home Page` - Navigate to home (resets state)
- `Create Warehouse` - Create warehouse with parameters
- `Add Items To Warehouse` - Add items to specific warehouse
- `Remove Items From Warehouse` - Remove items from warehouse
- `Delete Warehouse` - Delete warehouse by name
- `Get Warehouse Balance` - Retrieve current balance
- `Get Warehouse Free Space` - Get available capacity
- `Get Warehouse Progress Percentage` - Get progress bar value

## Maintenance

### Adding New Tests
1. Add new test case in `varasto_web.robot`
2. Use existing keywords or create new ones
3. Follow naming convention: Descriptive title with spaces
4. Include documentation string explaining test purpose
5. Run tests to verify

### Updating Selectors
If UI changes affect element selectors:
1. Locate XPath expressions in keyword definitions
2. Update to match new HTML structure
3. Test changes with `./run_robot_tests.sh`

### Troubleshooting
- **Tests timing out**: Increase wait times or check application startup
- **Element not found**: Verify XPath selectors match current HTML
- **Browser issues**: Ensure Chrome/Chromium is installed
- **Screenshots**: Check `robot-results/` for failure screenshots

## CI/CD Integration

To integrate with CI pipelines:
```yaml
# Example GitHub Actions step
- name: Run E2E Tests
  run: |
    ./run_robot_tests.sh
    
- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: robot-results
    path: robot-results/
```

## Best Practices

1. **Keep tests independent** - Each test should work in isolation
2. **Use meaningful names** - Test names should describe what they verify
3. **Document edge cases** - Explain why edge case tests exist
4. **Avoid hardcoded waits** - Use dynamic waits when possible
5. **Clean state between tests** - Ensure tests don't affect each other
6. **Capture screenshots** - SeleniumLibrary does this automatically on failure

## Resources

- [Robot Framework Documentation](https://robotframework.org/robotframework/)
- [SeleniumLibrary Documentation](https://robotframework.org/SeleniumLibrary/)
- [Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
