# Project: WHOOP + Garmin Health Hub

## 1. Project goal

Build a non-commercial privacy-first Telegram Mini App that combines health
and fitness data from WHOOP and Garmin into one unified service.

The application should:
- connect to a user's WHOOP account;
- connect to a user's Garmin account;
- retrieve health/fitness data;
- normalize data from both providers;
- calculate derived metrics;
- store a compact normalized history locally on the user's device;
- display statistics, trends and comparisons in one mobile-first interface.

The project is intended ONLY for use inside Telegram Mini Apps.
Do not build a standalone website product or separate user account system.

## 2. User identity

Telegram is the application's authentication layer.

When the Mini App opens inside Telegram:
- identify the user through the Telegram Mini App context / Telegram user ID;
- do not ask the user for an application username or password;
- do not create email/password authentication for our service;
- isolate all local application data by Telegram user.

The Telegram user identity is the primary application identity.

## 3. Hosting

The project will run on a rented hosting/server environment.

The same environment should host:
- the Telegram Mini App frontend;
- the Python backend/API;
- OAuth callback endpoints;
- other required application services.

GitHub Pages is NOT required.

The frontend should be served from our own hosted URL, which is configured
as the Telegram Mini App URL.

## 4. Architecture

High-level architecture:

Telegram
    ↓
Telegram Mini App
    ↓
Python backend
    ├── WHOOP integration
    ├── Garmin integration
    ├── data normalization
    ├── calculations
    └── business logic
    ↓
processed compact data
    ↓
Telegram Mini App
    ↓
Telegram DeviceStorage

The backend should be stateless whenever technically possible.

Do NOT introduce a server-side health-data database unless a concrete
technical requirement makes it necessary and the decision is discussed first.

The long-term health history should remain on the user's device.

## 5. Local storage and privacy

Use Telegram DeviceStorage for:
- normalized health history;
- application state;
- user preferences;
- other non-sensitive local data.

Use Telegram SecureStorage for sensitive tokens/credentials whenever
technically appropriate.

The DeviceStorage limit must be considered when designing the internal
data model.

Do not store raw WHOOP/Garmin API responses unnecessarily.

Instead:

provider API
→ validation
→ normalization
→ processing
→ compact internal data model
→ DeviceStorage

Optimize the internal format for long-term storage.

The backend must NOT:
- create a permanent health-data database;
- log health data;
- cache health data unnecessarily;
- send health data to analytics or unrelated third parties;
- write health data to persistent files unless explicitly required.

Health data may exist in backend memory temporarily while processing a request.

## 6. WHOOP integration

Use the official WHOOP OAuth 2.0 API.

Do NOT ask users to manually copy WHOOP API keys.

User flow:

Telegram Mini App
→ "Connect WHOOP"
→ WHOOP authorization page
→ user logs into WHOOP
→ user grants requested permissions
→ WHOOP redirects to our registered OAuth callback
→ backend exchanges authorization code for tokens
→ account becomes connected.

Request only the WHOOP scopes actually required by the application.

Keep WHOOP Client Secret exclusively on the backend.

Use access tokens for API requests and refresh tokens for continued access.

Never expose WHOOP Client Secret in frontend code.

Do not ask users for their WHOOP password.

Implement token refresh and revocation correctly.

## 7. Garmin integration

The official Garmin Health API is not assumed to be available for this
project.

For this project evaluate and use the available Python Garmin Connect
libraries:

1. python-garminconnect
2. garmy

Do not automatically choose one before evaluating both.

Compare them by:
- reliability;
- current maintenance/activity;
- authentication stability;
- MFA support;
- available health metrics;
- number and quality of API methods;
- rate limiting;
- token/session management;
- error handling;
- performance;
- implementation complexity;
- suitability for multiple users;
- long-term maintainability;
- resistance to Garmin Connect changes.

Build a small isolated Garmin adapter layer so the rest of the application
does not depend directly on either library.

The final choice between python-garminconnect and garmy must be made after
practical testing and comparison.

## 8. Garmin authentication

The initial Garmin connection may require the user's Garmin email and
password because the selected third-party libraries use Garmin Connect
authentication rather than the official Garmin Health API.

The intended flow is:

Telegram Mini App
→ "Connect Garmin"
→ user enters Garmin email/password into our secure HTTPS form
→ backend performs the library's authentication flow
→ Garmin authentication produces reusable OAuth/session tokens
→ backend uses those tokens for subsequent Garmin requests.

IMPORTANT:
- Never log Garmin passwords.
- Never store Garmin passwords in plaintext.
- Never put Garmin credentials into frontend source code.
- Never commit credentials to Git.
- Do not persist the password after the initial authentication request.
- Prefer persistent token/session credentials after successful login.
- Protect stored Garmin tokens as sensitive credentials.
- Support MFA if the selected library provides it.
- If the library can authenticate without repeatedly receiving the password,
  use the token/session mechanism instead.

The user should be able to disconnect Garmin and invalidate/remove stored
credentials/tokens where technically possible.

## 9. Provider abstraction

WHOOP and Garmin must be separate integrations.

Create a provider abstraction/interface so the application can work with:

WHOOP provider
Garmin provider

without mixing provider-specific API code with business logic.

Provider adapters should be responsible for:
- authentication;
- API requests;
- provider-specific response parsing;
- provider-specific error handling.

The rest of the application should work with normalized internal models.

## 10. Data normalization

WHOOP and Garmin may use different definitions, units, timestamps and
calculation methods.

Never assume that similarly named metrics are equivalent.

Normalize:
- units;
- timestamps/time zones;
- dates;
- metric naming;
- data structures.

Preserve provider-specific information where it is meaningful.

Document important differences between WHOOP and Garmin metrics.

## 11. Data processing

Python is the primary programming language.

Use Python for:
- backend;
- API integrations;
- authentication logic;
- data processing;
- normalization;
- calculations;
- business logic.

Keep processing logic in small, testable Python functions.

Separate:
API communication
from
data processing
from
presentation.

The backend should return only the minimum processed data required by the
Mini App.

## 12. Telegram Mini App

Use the current official Telegram Mini App APIs.

The application must:
- work only inside Telegram;
- use Telegram user context;
- use DeviceStorage for local history;
- use SecureStorage for sensitive values when appropriate;
- support Telegram themes;
- support mobile viewport and safe areas;
- be responsive and mobile-first.

Do not implement a separate website login.

## 13. Frontend

The frontend is the Telegram Mini App interface.

First prioritize:
- correct authentication;
- WHOOP connection;
- Garmin connection;
- data retrieval;
- normalization;
- local storage;
- correct statistics.

After the core functionality is stable, develop the final visual design.

The frontend should not contain provider-specific business logic unless
technically necessary.

## 14. Security

This project handles sensitive health information.

Security and privacy have high priority.

Rules:
- HTTPS everywhere.
- Never commit secrets.
- Never expose API client secrets.
- Never log passwords or tokens.
- Never log unnecessary health data.
- Validate Telegram Mini App authentication data on the backend when required.
- Validate all data received from clients.
- Protect OAuth callbacks against CSRF/state attacks.
- Use secure token storage.
- Minimize data sent to the backend.
- Minimize data returned to the frontend.
- Do not use third-party analytics that collect health information.

## 15. Testing

Important processing functions must have automated tests.

Provider integrations should have mocked tests where possible.

Do not run tests against real user accounts by default.

Never include real health data, credentials or tokens in the repository.

Use synthetic/test data for development.

## 16. Development workflow

For every significant task:

1. Inspect the existing project.
2. Inspect relevant official/provider documentation.
3. Briefly explain the proposed approach.
4. Implement the smallest reasonable change.
5. Run relevant tests/checks.
6. Report what changed and any remaining problems.

For major architectural changes:
- explain why the change is needed;
- explain alternatives;
- wait for approval before making a large architectural change.

Do not rewrite working code unnecessarily.

Do not add dependencies without a clear reason.

Do not introduce a database or additional infrastructure simply because
it is a common industry pattern.

## 17. Project priorities

Priority order:

1. Privacy
2. Security
3. Correctness of health data
4. Reliability of WHOOP/Garmin integrations
5. Simple architecture
6. Maintainability
7. Performance
8. UI/UX

This is a non-commercial project.

Prefer a simple, understandable architecture over enterprise-scale
infrastructure.