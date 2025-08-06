# Environment Configuration Setup

This guide explains how to set up environment variables for the VectorShift Integrations project.

## Quick Setup

1. **Copy the example environment file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit the `.env` file with your actual credentials:**
   ```bash
   # Open .env in your editor and replace the placeholder values
   ```

## Environment Variables

### Required for HubSpot Integration

```bash
HUBSPOT_CLIENT_ID=your-actual-hubspot-client-id
HUBSPOT_CLIENT_SECRET=your-actual-hubspot-client-secret
```

### Optional for Testing Other Integrations

```bash
# Notion (if you want to test Notion integration)
NOTION_CLIENT_ID=your-notion-client-id
NOTION_CLIENT_SECRET=your-notion-client-secret

# Airtable (if you want to test Airtable integration)
AIRTABLE_CLIENT_ID=your-airtable-client-id
AIRTABLE_CLIENT_SECRET=your-airtable-client-secret
```

### Optional Redis Configuration

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Getting OAuth Credentials

### HubSpot
1. Go to [HubSpot Developer Portal](https://developers.hubspot.com/)
2. Create a developer account
3. Create a new app
4. Configure OAuth settings:
   - **Redirect URL**: `http://localhost:8000/integrations/hubspot/oauth2callback`
   - **Scopes**: `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.objects.deals.read`
5. Copy the Client ID and Client Secret to your `.env` file

### Notion (Optional)
1. Go to [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Configure OAuth settings:
   - **Redirect URL**: `http://localhost:8000/integrations/notion/oauth2callback`
4. Copy the OAuth Client ID and Client Secret to your `.env` file

### Airtable (Optional)
1. Go to [Airtable Developers](https://airtable.com/developers/web/api/oauth-reference)
2. Create a new OAuth app
3. Configure OAuth settings:
   - **Redirect URL**: `http://localhost:8000/integrations/airtable/oauth2callback`
4. Copy the Client ID and Client Secret to your `.env` file

## Security Notes

- **Never commit your `.env` file to version control**
- The `.env` file is already included in `.gitignore`
- Use different credentials for development, staging, and production
- Rotate credentials regularly
- Use environment-specific `.env` files if needed

## Running the Application

After setting up your `.env` file:

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis
redis-server

# Start the backend
uvicorn main:app --reload
```

## Troubleshooting

### "Missing credentials" error
- Ensure your `.env` file exists in the `backend/` directory
- Check that variable names match exactly (case-sensitive)
- Verify there are no extra spaces around the `=` sign
- Make sure the `.env` file has actual values, not placeholder text

### Integration not working
- Verify your OAuth app is properly configured
- Check that redirect URLs match exactly
- Ensure required scopes are granted
- Check the application logs for specific error messages

### Redis connection issues
- Ensure Redis is running: `redis-server`
- Check Redis configuration in `.env`
- Verify Redis is accessible on the specified host/port
