# OMS – API Test Plan

## 1. Objective
Validate the correctness, stability, and data consistency of the Order Management System (OMS)
REST API that interacts with a real MongoDB database.

The focus is on API-level integration testing (no mocks), covering CRUD operations,
error handling, and basic API robustness.

---

## 2. Scope

### In Scope
- Orders API (`/orders`)
- CRUD operations:
  - Create order
  - Retrieve order by ID
  - Update order status
  - Delete order
- MongoDB data consistency validation
- Error handling for invalid and non-existent resources
- Idempotency / repeated operations behavior

### Out of Scope
- Authentication & authorization (JWT)
- Frontend (UI) testing
- Email notifications
- Real-time notifications
- Pagination and filtering (not implemented in the assignment)

---

## 3. Test Environment
- **API**: FastAPI
- **Database**: MongoDB (dedicated test database)
- **Test Framework**: pytest + requests
- **Execution**: Docker / docker-compose
- **CI**: GitHub Actions

Each test run uses an isolated MongoDB database.
Collections are cleaned between tests to ensure full isolation.

---

## 4. Test Types
- Integration API tests
- Database validation tests (post-API call verification)
- Negative tests (error handling)
- Basic robustness tests (invalid input, repeated operations)

---

## 5. Automated Test Scenarios

### Positive Scenarios
- Create a new order with valid data → returns order ID
- Retrieve an existing order by ID → returns correct data
- Update order status (Pending → Shipped) → status updated, items unchanged
- Delete an order → order removed from database

### Negative / Edge Scenarios
- Update non-existent order → `404 Not Found`
- Retrieve deleted order → `404 Not Found`
- Retrieve order with invalid ID format → `400 / 422`
- Delete the same order twice → second request returns `404` or idempotent `200`

---

## 6. Data Validation
- Order data returned by the API is validated against expected values
- Status updates do not modify immutable fields (e.g. items)
- Deleted orders are verified as removed by follow-up GET requests

---

## 7. Known Gaps / Improvement Suggestions
- Enforce order status transition rules (e.g. prevent invalid transitions)
- Add stricter business validations (negative price, empty items list)
- Add authentication & authorization tests once JWT is implemented
- Add pagination and filtering tests if endpoints are added

---

## 8. Bug Reporting Template (If Applicable)

**Title**: Short, descriptive summary  
**Endpoint**: HTTP method + endpoint  
**Steps to Reproduce**:
1. …
2. …

**Expected Result**:  
**Actual Result**:  
**Environment**: Local / CI  
**Logs / Evidence**: Response body, status code, screenshots if relevant

No functional bugs were found during the execution of the automated test suite.

