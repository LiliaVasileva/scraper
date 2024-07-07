from urllib.parse import urlparse, urlunparse


def normalize_url(url):
    parsed_url = urlparse(url)
    # Remove fragment and trailing slash
    normalized_path = parsed_url.path.rstrip('/')
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, normalized_path, '', '', ''))
    return normalized_url


def should_visit_url(link_url, start_url, visited_urls):
    normalized_link_url = normalize_url(link_url)
    normalized_start_url = normalize_url(start_url)
    return normalized_link_url not in visited_urls and urlparse(normalized_link_url).netloc == urlparse(
        normalized_start_url).netloc
