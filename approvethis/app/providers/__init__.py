"""Provider factory."""
from flask import current_app


_provider_instance = None


def get_provider():
    """
    Get the configured GitHub provider instance.
    
    Returns:
        GitHubProvider: Configured provider instance
    """
    global _provider_instance
    
    if _provider_instance is None:
        provider_type = current_app.config.get('GITHUB_PROVIDER', 'mock')
        
        if provider_type == 'mock':
            from app.providers.mock import MockGitHubProvider
            _provider_instance = MockGitHubProvider()
        elif provider_type == 'github':
            from app.providers.github import RealGitHubProvider
            # TODO: Get token from config
            _provider_instance = RealGitHubProvider()
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
    
    return _provider_instance


def reset_provider():
    """Reset provider instance (useful for testing)."""
    global _provider_instance
    _provider_instance = None
