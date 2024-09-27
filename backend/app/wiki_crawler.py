import logging
from typing import Set, Dict, List, Tuple
from bs4 import BeautifulSoup
from urllib.request import urlopen


class WikiCrawler:
    def get_first_sub_links(self, url: str, collected_links: Set[str], first_n_sublinks: int) -> Set[str]:
        sub_links = set()
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        counted_links = 0
        for a in soup.find_all('a', href=True):
            if (a["href"].startswith('/wiki/')
                and ":" not in a["href"]
                and "(identifier)" not in a["href"]) \
                    and a["href"] != "/wiki/Main_Page" \
                    and "https://en.wikipedia.org" + a["href"] != url:
                if "https://en.wikipedia.org" + a["href"] not in collected_links:
                    counted_links += 1

                sub_links.add("https://en.wikipedia.org" + a["href"])
                if counted_links >= first_n_sublinks:
                    return sub_links
                logging.info("found link: https://en.wikipedia.org" + a["href"])
        return sub_links

    def get_last_sub_links(self, url: str, collected_links: Set[str], last_n_sublinks: int) -> Set[str]:
        sub_links = set()
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        counted_links = 0
        for a in soup.find_all('a', href=True):
            if (a["href"].startswith('/wiki/')
                and ":" not in a["href"]
                and "(identifier)" not in a["href"]) \
                    and a["href"] != "/wiki/Main_Page" \
                    and "https://en.wikipedia.org" + a["href"] != url:
                sub_links.add("https://en.wikipedia.org" + a["href"])
                logging.info("https://en.wikipedia.org" + a["href"])
        last_sub_links = set()
        for link in sub_links:
            last_sub_links.add(link)
            if link not in collected_links:
                counted_links += 1
            if counted_links >= last_n_sublinks:
                return last_sub_links
        return set(list(sub_links)[-last_n_sublinks:])

    def convert_links_to_d3_nodes(self, sub_links: Set[str]) -> List[Dict[str, str]]:
        d3_nodes = []
        for sub_link in sub_links:
            d3_nodes.append({"id": sub_link})
        return d3_nodes

    def convert_links_and_sub_links_to_d3_nodes_and_links(self,
                                                          sub_links: Set[str],
                                                          links: List[Tuple[str, str]]
                                                          ) -> (Dict, Dict):
        d3_nodes = []
        d3_links = []
        for link in links:
            if link[0] not in sub_links:
                sub_links.add(link[0])
                continue
            if link[1] not in sub_links:
                sub_links.add(link[1])
                continue
            d3_links.append({"source": link[0], "target": link[1]})
        for sub_link in sub_links:
            d3_nodes.append({"id": sub_link})
        return d3_nodes, d3_links


if __name__ == "__main__":
    crawler = WikiCrawler()
    sub_lists_dict, links = crawler.walk_sub_links(
        'https://en.wikipedia.org/wiki/Epidemiology_of_depression', 5, 5)
    print(links)
    d3_nodes, d3_links = crawler.convert_links_and_sub_links_to_d3_nodes_and_links(sub_lists_dict, links)
    print(d3_nodes)
    print(d3_links)
    # sub_links = {}
    # next_frontier = []
    # url = 'https://en.wikipedia.org/wiki/Epidemiology_of_depression'
    # html = urlopen(url)
    # soup = BeautifulSoup(html, 'html.parser')
    # for a in soup.find_all('a', href=True):
    #     if (a["href"].startswith('/wiki/')
    #         and ":" not in a["href"]
    #         and "(identifier)" not in a["href"]) \
    #             and a["href"] != "/wiki/Main_Page" \
    #             and "https://en.wikipedia.org" + a["href"] != url:
    #         print("https://en.wikipedia.org" + a["href"])
    #         next_frontier.append("https://en.wikipedia.org" + a["href"])
    #         sub_links[a.text] = a["href"]
