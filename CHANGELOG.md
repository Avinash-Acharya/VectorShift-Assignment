# Changelog

All notable changes to the VectorShift Integrations project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
<!-- New features -->

### Changed
<!-- Changes in existing functionality -->

### Deprecated
<!-- Soon-to-be removed features -->

### Removed
<!-- Removed features -->

### Fixed
<!-- Bug fixes -->

### Security
<!-- Vulnerability fixes -->

---

## Format Guidelines

### Version Format
- Use [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH
- Use [Unreleased] for changes not yet released
- Format: `## [1.0.0] - 2025-01-15`

### Categories
- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

### Entry Format
```markdown
### Added
- New OAuth integration for ServiceX
- User authentication with JWT tokens
- API rate limiting middleware

### Changed
- Updated React from v17 to v18
- Improved error handling in OAuth flow
- Modified database schema for better performance

### Fixed
- Fixed memory leak in Redis connection pool
- Resolved CORS issues with frontend requests
- Fixed pagination bug in data loading
```

### Breaking Changes
Mark breaking changes with ⚠️ emoji:
```markdown
### Changed
- ⚠️ **BREAKING**: Updated Pydantic to v2 (requires model migration)
- ⚠️ **BREAKING**: Changed API response format for `/oauth/callback`
```

### Migration Notes
Include migration instructions for major changes:
```markdown
### Migration Required
1. Update package.json dependencies
2. Migrate Pydantic v1 models to v2 syntax
3. Update React Root API calls
```

---

<!-- 
Example entries for reference:

## [1.0.0] - 2025-01-15
### Added
- Initial OAuth 2.0 integration for Airtable and Notion
- React frontend with Material-UI components
- FastAPI backend with Redis session storage

### Security
- Implemented PKCE for OAuth 2.0 flows
- Added CORS protection for API endpoints
-->
