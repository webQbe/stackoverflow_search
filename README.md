# Custom Search Engine for StackOverflow

- Implementing back-end features from [Python Google Search Filter](https://github.com/webQbe/google_search_filter)
- Implementing front-end feautures from [Wikipedia Search App](https://github.com/webQbe/js_search_app)
- Using StackExchange API

## Getting StackExchange API Key

1. Create an account & log in to https://stackapps.com/ 
2. Register app at https://stackapps.com/apps/oauth/register
3. Get API Key

## Prevent unnecessary page reload by VSCode Live Server
Open VSCode →  Settings → Extensions → Live Server → Ignore Files and add these patterns:
    ```
    {
        "liveServer.settings.ignoreFiles": [
            "**/*.py",
            "**/*.db",
            "**/back/**",
            "**/.git/**"
        ]
    }
    ```