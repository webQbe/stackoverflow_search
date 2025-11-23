# Custom Search Engine for StackOverflow

- Implement Google Custom Search API to search StackOverflow
- Rank and filter search results by relevance and store them in the backend
- Build UI to Collect search input, fetch and output the results

## About
Built from scratch using concepts learned from following tutorials:
- [Wikipedia Search App by Dave Gray](https://github.com/webQbe/js_search_app) (front-end features)
- [Python Google Search Filter by Dataquest](https://github.com/webQbe/google_search_filter)(back-end features)

This is my implementation and learning exercise — credit given above.

### Getting Started
1. Create an account & log in to https://stackapps.com/ 
2. Register app at https://stackapps.com/apps/oauth/register
3. Get API Key

#### Prevent unnecessary page reload by VSCode Live Server
- Open VSCode →  Settings → Extensions → Live Server → Ignore Files and add these patterns:

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

## License
MIT License
