import os
import pytest
import json
from typing import Callable, Counter, Optional
from webpage_parser import WebpageParser, ArgumentNotProvided


@pytest.fixture
def web_parser() -> WebpageParser:
    '''Returns a WebpageParser object with root link'''
    return WebpageParser('https://www.globalapptesting.com/')


@pytest.fixture
def web_parser_without_root() -> WebpageParser:
    '''Returns a WebpageParser object without root link'''
    return WebpageParser('')


@pytest.fixture
def root_link() -> str:
    return 'https://www.globalapptesting.com'


@pytest.fixture
def build_path() -> Callable[[], str]:
    '''Build path to the file in the directory with test data'''
    def builder_func(file_name: str, format: Optional[str] = None) -> str:
        file = f'{file_name}.{format}' if format else f'{file_name}'
        return os.path.join('test_data', file)
    return builder_func


@pytest.fixture
def graph_edges() -> list:
    return [('https://www.globalapptesting.com/', 'https://www.globalapptesting.com/product', 7),
            ('https://www.globalapptesting.com/',
             'https://www.globalapptesting.com/platform/integrations', 5),
            ('https://www.globalapptesting.com/', 'https://www.globalapptesting.com/resources/resource-library',
             4), ('https://www.globalapptesting.com/', 'https://www.globalapptesting.com/terms-and-conditions', 1),
            ('https://www.globalapptesting.com/', 'https://www.globalapptesting.com/code-of-conduct', 1)]


@ pytest.fixture
def temp_graph_dict() -> dict:
    return {'https://www.globalapptesting.com/': [('https://www.globalapptesting.com', 'https://www.globalapptesting.com', 1), ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/product', 7),
                                                  ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/platform/test-management', 2), (
                                                      'https://www.globalapptesting.com', 'https://www.globalapptesting.com/platform/test-execution', 2),
                                                  ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/platform/test-results-analysis',
                                                   2), ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/platform/integrations', 5),
                                                  ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/solutions', 2), ('https://www.globalapptesting.com', 'https://www.globalapptesting.com/on-demand-test-case-execution-jira-integration', 2)]}


@pytest.fixture
def temp_graph_dict_full(build_path) -> dict:
    file_name = 'test_graph_dict_full'
    file_path = build_path(file_name, 'json')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        try:
            graph_dict_full = json.load(fhandle)
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')
    return graph_dict_full


@ pytest.fixture
def expected_json_sample() -> json:
    return {
        "https://www.globalapptesting.com/": [
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com",
                122222222222222
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/product/",
                1000212875982
            ]
        ]
    }


@ pytest.fixture
def small_map_sample() -> dict:
    return {'https://www.globalapptesting.com/': {'internal_links': Counter({'https://www.globalapptesting.com/product': 70, 'https://www.globalapptesting.com/platform/integrations': 5, 'https://www.globalapptesting.com/resources/resource-library': 4, 'https://www.globalapptesting.com/about-us': 4}),
                                                  'external_links': Counter({'https://www.leadingqualitybook.com/': 2, 'https://testathon.co/': 2, 'https://www.facebook.com/globalapptesting/': 1}),
                                                  'dead_links': Counter(),
                                                  'phone_links': Counter(),
                                                  'email_links': Counter()}}


@ pytest.fixture
def temp_map_dict() -> dict:
    '''Return map_dict like test data'''
    return {'https://www.globalapptesting.com/': {'internal_links': Counter({'https://www.globalapptesting.com/product': 7, 'https://www.globalapptesting.com/platform/integrations': 5, 'https://www.globalapptesting.com/resources/resource-library': 4,
                                                                             'https://www.globalapptesting.com/terms-and-conditions': 1, 'https://www.globalapptesting.com/code-of-conduct': 1}),
                                                  'external_links': Counter({'https://www.leadingqualitybook.com/': 2, 'https://testathon.co/': 2, 'https://www.facebook.com/globalapptesting/': 1, 'https://www.linkedin.com/company/global-app-testing': 1, 'https://twitter.com/qaops?lang=en': 1,
                                                                             'https://www.g2.com/products/global-app-testing/reviews?utm_source=review-widget': 1}),
                                                  'dead_links': Counter(), 'phone_links': Counter(), 'email_links': Counter(), 'file_links': Counter(),
                                                  'HTTP_STATUS': 200},
            'https://www.globalapptesting.com/product': {'internal_links': Counter({'https://www.globalapptesting.com/product': 4, 'https://www.globalapptesting.com/platform/integrations': 4, 'https://www.globalapptesting.com/resources/resource-library': 4, 'https://www.globalapptesting.com/about-us': 4,
                                                                                    'https://www.globalapptesting.com/on-demand-test-case-execution-jira-integration': 2, 'https://www.globalapptesting.com/on-demand-test-case-execution-github-integration': 2, 'https://www.globalapptesting.com/on-demand-test-case-execution-testrail-integration': 2}),
                                                         'external_links': Counter({'https://www.leadingqualitybook.com/': 2, 'https://testathon.co/': 2, 'https://cta-redirect.hubspot.com/cta/redirect/540930/33915d8b-4806-48e9-9756-29171861ac9c': 1, 'https://www.facebook.com/globalapptesting/': 1, 'https://www.linkedin.com/company/global-app-testing': 1,
                                                                                    'https://twitter.com/qaops?lang=en': 1, 'https://www.g2.com/products/global-app-testing/reviews?utm_source=review-widget': 1}),
                                                         'dead_links': Counter(), 'phone_links': Counter(), 'email_links': Counter(), 'file_links': Counter(), 'HTTP_STATUS': 200},
            'https://www.globalapptesting.com/platform/test-management': {'internal_links': Counter({'https://www.globalapptesting.com/product': 4, 'https://www.globalapptesting.com/platform/integrations': 4, 'https://www.globalapptesting.com/resources/resource-library': 4, 'https://www.globalapptesting.com/about-us': 4,
                                                                                                     'https://www.globalapptesting.com/code-of-conduct': 1}),
                                                                          'external_links': Counter({'https://www.leadingqualitybook.com/': 2, 'https://testathon.co/': 2, 'https://cta-redirect.hubspot.com/cta/redirect/540930/33915d8b-4806-48e9-9756-29171861ac9c': 1, 'https://www.facebook.com/globalapptesting/': 1,
                                                                                                     'https://www.linkedin.com/company/global-app-testing': 1, 'https://twitter.com/qaops?lang=en': 1, 'https://www.g2.com/products/global-app-testing/reviews?utm_source=review-widget': 1}),
                                                                          'dead_links': Counter(), 'phone_links': Counter(), 'email_links': Counter(), 'file_links': Counter(), 'HTTP_STATUS': 200}}


@ pytest.fixture
def expected_json() -> dict:
    return {
        "https://www.globalapptesting.com/": [
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com",
                1
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/product",
                7
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/platform/test-management",
                2
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/platform/test-execution",
                2
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/platform/test-results-analysis",
                2
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/platform/integrations",
                5
            ],
            [
                "https://www.globalapptesting.com",
                "https://www.globalapptesting.com/functional-testing/test-case-execution",
                2
            ]
        ]
    }


@pytest.fixture
def write_to_json_file(build_path):

    def inner_func(file_name: str, expected_json_sample: json):
        file_path = build_path(file_name, 'json')
        with open(file=file_path, mode='w', encoding='utf8') as fhandle:
            try:
                json.dump(expected_json_sample, fhandle, indent=4)
            except Exception as exc:
                print(
                    f'Exception occured when trying to write to json file {file_path}: {exc}')
    return inner_func


@pytest.fixture
def expected_incoming_count_links() -> dict:
    return {'https://www.globalapptesting.com': 360, 'https://www.globalapptesting.com/product': 360, 'https://www.globalapptesting.com/platform/test-management': 360, 'https://www.globalapptesting.com/platform/test-execution': 360, 'https://www.globalapptesting.com/platform/test-results-analysis': 360, 'https://www.globalapptesting.com/platform/integrations': 360, 'https://www.globalapptesting.com/solutions': 360, 'https://www.globalapptesting.com/on-demand-test-case-execution-jira-integration': 316, 'https://www.globalapptesting.com/on-demand-test-case-execution-github-integration': 316, 'https://www.globalapptesting.com/on-demand-test-case-execution-testrail-integration': 316,
            'https://www.globalapptesting.com/on-demand-test-case-execution-zephyr-squad-integration': 316, 'https://www.globalapptesting.com/on-demand-test-case-execution-slack-integration': 316, 'https://www.globalapptesting.com/how-we-help/cio-cto': 360, 'https://www.globalapptesting.com/how-we-help/engineering-teams': 360, 'https://www.globalapptesting.com/how-we-help/qa-teams': 360, 'https://www.globalapptesting.com/how-we-help/increase-release-velocity': 360, 'https://www.globalapptesting.com/how-we-help/improve-product-quality': 360, 'https://www.globalapptesting.com/how-we-help/localise-qa-coverage': 360, 'https://www.globalapptesting.com/how-we-help/maximise-team-productivity': 360,
            'https://www.globalapptesting.com/functional-testing/exploratory-tests': 360, 'https://www.globalapptesting.com/functional-testing/test-case-execution': 360, 'https://www.globalapptesting.com/solutions/usability-testing': 360, 'https://www.globalapptesting.com/functional-testing/mobile': 360, 'https://www.globalapptesting.com/functional-testing/web': 360, 'https://www.globalapptesting.com/pricing': 361, 'https://www.globalapptesting.com/resources/resource-library': 360, 'https://www.globalapptesting.com/blog': 360, 'https://www.globalapptesting.com/customers': 360, 'https://www.globalapptesting.com/engineering': 360, 'https://www.globalapptesting.com/about-us': 360,
            'https://www.globalapptesting.com/careers': 360, 'https://www.globalapptesting.com/company/partners': 360, 'https://www.globalapptesting.com/security': 360, 'https://www.globalapptesting.com/our-testers': 360, 'https://www.globalapptesting.com/contact': 361, 'https://www.globalapptesting.com/news': 360, 'https://www.globalapptesting.com/privacy-policy': 361, 'https://www.globalapptesting.com/terms-and-conditions': 360, 'https://www.globalapptesting.com/code-of-conduct': 360, 'https://www.globalapptesting.com/careers/privacy': 1, 'https://www.globalapptesting.com/engineering/careers': 44, 'https://www.globalapptesting.com/engineering/designing-an-interface-for-hierarchical-environments': 15,
            'https://www.globalapptesting.com/blog/topic/data-science': 40, 'https://www.globalapptesting.com/engineering/5-best-practices-to-accelerate-code-review': 17, 'https://www.globalapptesting.com/blog/topic/increasing-speed': 104, 'https://www.globalapptesting.com/blog/topic/engineering': 128, 'https://www.globalapptesting.com/engineering/lets-take-a-closer-look-at-the-tests-created-in-rspec': 17, 'https://www.globalapptesting.com/blog/topic/ruby': 40, 'https://www.globalapptesting.com/engineering/implementing-packwerk-to-delimit-bounded-contexts': 9, 'https://www.globalapptesting.com/engineering/activerecord-models-how-to-remove-data-in-gdpr-compliant-way': 9,
            'https://www.globalapptesting.com/engineering/reinforcement-learning-for-web-testing-at-global-app-testing': 33, 'https://www.globalapptesting.com/engineering/gat-techtalk-4-ddd-in-ruby': 7, 'https://www.globalapptesting.com/engineering/rails-monolith-modularisation-with-cqrs': 32, 'https://www.globalapptesting.com/engineering/design-the-unknown-with-the-help-of-event-storming': 10, 'https://www.globalapptesting.com/blog/topic/inside-gat': 119, 'https://www.globalapptesting.com/engineering/when-gat-containerised-krakow': 9, 'https://www.globalapptesting.com/engineering/page/2': 2, 'https://www.globalapptesting.com/engineering/tag/engineering': 32, 'https://www.globalapptesting.com/engineering/tag/ruby': 32,
            'https://www.globalapptesting.com/engineering/tag/inside-gat': 32, 'https://www.globalapptesting.com/engineering/tag/data-science': 32, 'https://www.globalapptesting.com/engineering/tag/increasing-speed': 32, 'https://www.globalapptesting.com/engineering/event-storming-agile-success': 32, 'https://www.globalapptesting.com/blog/software-observability': 162, 'https://www.globalapptesting.com/blog/demand-testing-what-is-it': 162, 'https://www.globalapptesting.com/blog/apple-bug-safari-ios': 162, 'https://www.globalapptesting.com/blog/automated-functional-testing': 7, 'https://www.globalapptesting.com/blog/ad-hoc-testing': 14, 'https://www.globalapptesting.com/blog/topic/improving-quality': 87,
            'https://www.globalapptesting.com/blog/topic/growth-via-qa': 87, 'https://www.globalapptesting.com/blog/topic/ad-hoc-testing': 85, 'https://www.globalapptesting.com/blog/beta-testing-software': 11, 'https://www.globalapptesting.com/blog/topic/beta-testing': 85, 'https://www.globalapptesting.com/blog/5-critical-mistakes-to-avoid-in-your-qa-testing-process': 9, 'https://www.globalapptesting.com/blog/topic/qaops': 87, 'https://www.globalapptesting.com/blog/top-10-mobile-usability-testing-methods-every-qa-tester-should-know': 8, 'https://www.globalapptesting.com/blog/a-framework-for-qa-test-planning': 9, 'https://www.globalapptesting.com/blog/the-ultimate-guide-to-smoke-testing': 4,
            'https://www.globalapptesting.com/blog/page/2': 3, 'https://www.globalapptesting.com/blog/topic/events': 85, 'https://www.globalapptesting.com/blog/topic/customer-experience': 85, 'https://www.globalapptesting.com/blog/the-women-who-changed-the-tech-world': 85, 'https://www.globalapptesting.com/blog/qa-process': 88, 'https://www.globalapptesting.com/blog/top-software-qa-blogs': 85, 'https://www.globalapptesting.com/blog/author/sam-ernest-jones': 3, 'https://www.globalapptesting.com/blog/global-app-testing-part-of-tech-nation-future-fifty-9.0': 11, 'https://www.globalapptesting.com/blog/author/sam-ernest-jones/page/0': 2, 'https://www.globalapptesting.com/blog/how-to-build-the-ultimate-qa-strategy': 15,
            'https://www.globalapptesting.com/': 34, 'https://www.globalapptesting.com/best-practices-for-qa-testing': 33, 'https://www.globalapptesting.com/best-practices-automated-testing': 24, 'https://www.globalapptesting.com/blog/how-to-implement-test-automation-for-the-first-time': 12, 'https://www.globalapptesting.com/blog/crowdsourced-testing-packs-a-punch-over-in-house-qa': 10, 'https://www.globalapptesting.com/blog/author/fahim-sachedina': 53, 'https://www.globalapptesting.com/blog/the-true-cost-of-failing-to-put-your-customers-first': 20, 'https://www.globalapptesting.com/blog/remote-working-has-changed-software-development-forever.-heres-why': 6,
            'https://www.globalapptesting.com/blog/how-to-avoid-high-impact-risks-in-qa-delivery': 5, 'https://www.globalapptesting.com/blog/what-partnering-with-a-qa-solution-means-for-your-team': 9, 'https://www.globalapptesting.com/blog/whats-keeping-your-qa-team-up-at-night': 5, 'https://www.globalapptesting.com/blog/tech-trends-for-2020-and-beyond': 5, 'https://www.globalapptesting.com/blog/the-issues-that-tech-leaders-are-facing-in-2020': 6, 'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/2': 3, 'https://www.globalapptesting.com/blog/the-worlds-first-computer-bug-global-app-testing': 3, 'https://www.globalapptesting.com/customers/facebook': 1, 'https://www.globalapptesting.com/customers/canva': 3,
            'https://www.globalapptesting.com/customers/livesafe': 6, 'https://www.globalapptesting.com/customers/acasa': 1, 'https://www.globalapptesting.com/best-practices-crowdtesting': 13, 'https://www.globalapptesting.com/regression-testing-guide': 14, 'https://www.globalapptesting.com/best-practices-functional-testing': 11, 'https://www.globalapptesting.com/best-practices-localization-testing': 12, 'https://www.globalapptesting.com/best-practices-exploratory-testing': 20, 'https://www.globalapptesting.com/manual-testing-best-practices': 19, 'https://www.globalapptesting.com/the-ultimate-guide-to-agile-testing': 9, 'https://www.globalapptesting.com/blog/the-critical-role-exploratory-testing-plays-in-agile-teams': 12,
            'https://www.globalapptesting.com/blog/key-qa-and-testing-takeaways-from-the-agile-manifesto': 6, 'https://www.globalapptesting.com/blog/doing-agile-testing-properly-how-metrics-can-help': 5, 'https://www.globalapptesting.com/blog/agile-testing-microphone-critical': 5, 'https://www.globalapptesting.com/blog/how-bugs-impact-your-company-infographic': 5, 'https://www.globalapptesting.com/contact-sales': 13, 'https://www.globalapptesting.com/blog/author/nick-roberts': 25, 'https://www.globalapptesting.com/blog/recreate-customers-bugs': 5, 'https://www.globalapptesting.com/blog/remote-working-qa-team-prepared': 10, 'https://www.globalapptesting.com/blog/twitters-most-trending-emojis-will-bring-your-apps-to-life': 5,
            'https://www.globalapptesting.com/blog/book-announcement-leading-quality': 7, 'https://www.globalapptesting.com/blog/picking-apart-stackoverflow-what-bugs-developers-the-most': 7, 'https://www.globalapptesting.com/blog/top-5-localization-challenges': 11, 'https://www.globalapptesting.com/blog/announcing-global-app-testing-tech-talk-episode-1': 6, 'https://www.globalapptesting.com/blog/what-to-do-when-you-have-a-poor-quality-enterprise-app': 9, 'https://www.globalapptesting.com/blog/developing-apps-internet-of-things-iot': 5, 'https://www.globalapptesting.com/blog/what-do-meltdown-and-spectre-mean-for-software-testing': 5, 'https://www.globalapptesting.com/blog/author/nick-roberts/page/2': 3,
            'https://www.globalapptesting.com/blog/topic/beta-testing/page/0': 2, 'https://www.globalapptesting.com/blog/topic/ad-hoc-testing/page/0': 2, 'https://www.globalapptesting.com/blog/empower-your-team-a-story-about-the-right-team-structure-to-achieve-continuous-delivery': 23, 'https://www.globalapptesting.com/blog/topic/engineering/page/0': 2, 'https://www.globalapptesting.com/blog/topic/customer-experience/page/0': 2, 'https://www.globalapptesting.com/blog/mwc-2020-unmissable-events-talks-workshops': 5, 'https://www.globalapptesting.com/blog/software-testing-qa-conferences-in-2020': 8, 'https://www.globalapptesting.com/blog/quality-leaders-network-edtech-breakfast-of-champions': 5,
            'https://www.globalapptesting.com/blog/eurostar-conference-2020-prague-the-complete-guide': 4, 'https://www.globalapptesting.com/blog/topic/events/page/0': 2, 'https://www.globalapptesting.com/blog/your-ultimate-guide-to-the-national-software-testing-conference': 8, 'https://www.globalapptesting.com/blog/what-weve-been-working-on-usability-improvements': 5, 'https://www.globalapptesting.com/blog/mwc-americas-ultimate-guide': 5, 'https://www.globalapptesting.com/blog/mobile-world-congress-2018': 5, 'https://www.globalapptesting.com/blog/bug-wars-gold-digger-edition': 8, 'https://www.globalapptesting.com/blog/more-than-just-values': 4, 'https://www.globalapptesting.com/blog/tester-for-a-day': 6,
            'https://www.globalapptesting.com/blog/topic/inside-gat/page/0': 2, 'https://www.globalapptesting.com/blog/what-is-exploratory-testing': 18, 'https://www.globalapptesting.com/blog/how-to-start-automation-testing-from-scratch': 6, 'https://www.globalapptesting.com/blog/regression-testing-while-cooking-a-curry': 6, 'https://www.globalapptesting.com/product/exploratory-testing': 2, 'https://www.globalapptesting.com/demo-request': 19, 'https://www.globalapptesting.com/product/mobile-app-testing': 2, 'https://www.globalapptesting.com/product/web-app-testing': 2, 'https://www.globalapptesting.com/platform/integrations/': 2, 'https://www.globalapptesting.com/blog/why-the-human-touch-is-still-crucial-in-automated-software-testing': 8,
            'https://www.globalapptesting.com/blog/why-is-automation-like-amusement-parks': 7, 'https://www.globalapptesting.com/blog/7-tips-to-improve-your-qa-operations': 6, 'https://www.globalapptesting.com/blog/testing-approach': 10, 'https://www.globalapptesting.com/-ab-variant-669a4747-8a18-4779-a977-d4a108c6b8e4': 6, 'https://www.globalapptesting.com/blog/can-you-qa-everything': 9, 'https://www.globalapptesting.com/blog/4-ways-to-create-a-quality-culture-in-your-company': 9, 'https://www.globalapptesting.com/blog/the-6-skills-needed-for-exceptional-exploratory-testing': 7, 'https://www.globalapptesting.com/blog/3-elements-you-need-to-succeed-at-exploratory-testing': 7, 'https://www.globalapptesting.com/company/global-testing-community': 4,
            'https://www.globalapptesting.com//go.globalapptesting.com/ebook-ultimate-guide-to-crowdsourced-testing': 1, 'https://www.globalapptesting.com/blog/author/tony-dolan': 12, 'https://www.globalapptesting.com/blog/the-6-secrets-of-app-stickiness': 6, 'https://www.globalapptesting.com/blog/5-qa-tips-every-proptech-company-needs-to-know': 6, 'https://www.globalapptesting.com/blog/bug-triage-is-it-delaying-your-releases': 8, 'https://www.globalapptesting.com/blog/how-to-harness-the-power-of-qa-for-company-growth': 7, 'https://www.globalapptesting.com/blog/how-to-get-your-app-approved-by-the-app-store': 6, 'https://www.globalapptesting.com/blog/software-testing-in-house-vs-crowd-testing': 6,
            'https://www.globalapptesting.com/blog/how-to-work-future-mobile-trends-into-your-development-strategy': 6, 'https://www.globalapptesting.com/blog/author/tony-dolan/page/2': 2, 'https://www.globalapptesting.com/blog/4-technology-trends-that-will-affect-qa-testing-in-2018': 4, 'https://www.globalapptesting.com/blog/author/tony-dolan/page/1': 2, 'https://www.globalapptesting.com/blog/author/tony-dolan/page/0': 1, 'https://www.globalapptesting.com/blog/how-to-cover-an-expanding-universe-of-device-and-os-complexity': 7, 'https://www.globalapptesting.com/blog/elastic-qa-what-is-it-and-why-do-you-need-it': 10, 'https://www.globalapptesting.com/blog/5-key-takeaways-from-elastic-qa': 6,
            'https://www.globalapptesting.com/blog/everything-there-is-to-know-about-automated-testing': 6, 'https://www.globalapptesting.com/blog/why-is-this-hairdresser-so-slow': 5, 'https://www.globalapptesting.com/blog/topic/increasing-speed/page/0': 2, 'https://www.globalapptesting.com/products/web-app-testing': 3, 'https://www.globalapptesting.com/blog/the-ultimate-guide-to-software-testing-when': 1, 'https://www.globalapptesting.com/blog/the-ultimate-guide-to-software-testing-who': 4, 'https://www.globalapptesting.com/blog/software-testing-in-house-vs-crowdsourced': 8, 'https://www.globalapptesting.com/blog/earn-digital-applause-draw-more-customers-to-your-app': 7, 'https://www.globalapptesting.com/blog/how-to-not-be-the-next-wirecard': 5,
            'https://www.globalapptesting.com/blog/author/camilla-mcdermott': 4, 'https://www.globalapptesting.com/blog/how-quality-became-a-growth-driver': 4, 'https://www.globalapptesting.com/blog/unlock-team-and-company-efficiencies-with-apis': 8, 'https://www.globalapptesting.com/blog/using-apis-to-leverage-crowdtesting': 8, 'https://www.globalapptesting.com/blog/author/camilla-mcdermott/page/0': 2, 'https://www.globalapptesting.com/blog/how-to-run-a-comprehensive-mobile-app-test': 6, 'https://www.globalapptesting.com/blog/software-testing-qa-trends-in-2020-and-the-next-decade': 8, 'https://www.globalapptesting.com/blog/5-testing-trends-that-will-shape-2019': 11, 'https://www.globalapptesting.com/blog/topic/qaops/page/2': 3,
            'https://www.globalapptesting.com/blog/software-testing': 4, 'https://www.globalapptesting.com/blog/what-ctos-must-know-about-qa-in-2018-infographic': 4, 'https://www.globalapptesting.com/blog/testing-metrics-how-to-demonstrate-the-value-of-testing-with-quantifiable-metrics': 7, 'https://www.globalapptesting.com/blog/what-is-continuous-testing': 3, 'https://www.globalapptesting.com/blog/topic/qaops/page/1': 2, 'https://www.globalapptesting.com/blog/topic/qaops/page/3': 1, 'https://www.globalapptesting.com/blog/how-do-you-ensure-quality-in-the-software-you-create': 12, 'https://www.globalapptesting.com/blog/perfect-app': 7, 'https://www.globalapptesting.com/blog/topic/growth-via-qa/page/2': 3,
            'https://www.globalapptesting.com/blog/our-first-quality-leaders-network-evening-global-app-testing': 5, 'https://www.globalapptesting.com/blog/3-characteristics-of-top-performing-apps': 5, 'https://www.globalapptesting.com/blog/types-of-software-testing': 6, 'https://www.globalapptesting.com/blog/3-essential-app-discoverability-strategies-for-the-ios-11-app-store': 3, 'https://www.globalapptesting.com/blog/a-guide-to-outsourced-software-testing': 3, 'https://www.globalapptesting.com/blog/zawgyi-vs-unicode': 5, 'https://www.globalapptesting.com/blog/topic/growth-via-qa/page/1': 2, 'https://www.globalapptesting.com/blog/topic/growth-via-qa/page/3': 1, 'https://www.globalapptesting.com/blog/7-strategies-build-the-perfect-app': 4,
            'https://www.globalapptesting.com/blog/mobile-app-testing-at-scale': 4, 'https://www.globalapptesting.com/blog/topic/growth-via-qa/page/0': 1, 'https://www.globalapptesting.com/blog/topic/improving-quality/page/2': 3, 'https://www.globalapptesting.com/blog/how-to-increase-e-commerce-sales-with-quality': 6, 'https://www.globalapptesting.com/blog/our-first-quality-leaders-network-breakfast': 4, 'https://www.globalapptesting.com/blog/6-step-guide-to-avoiding-one-star-reviews-of-your-app': 7, 'https://www.globalapptesting.com/blog/topic/improving-quality/page/1': 2, 'https://www.globalapptesting.com/blog/topic/improving-quality/page/3': 2, 'https://www.globalapptesting.com/blog/how-to-prevent-a-212-million-bug': 3,
            'https://www.globalapptesting.com/blog/pixels-and-iphones-testing-on-new-devices': 4, 'https://www.globalapptesting.com/blog/when-the-coffee-maker-breaks': 3, 'https://www.globalapptesting.com/blog/is-software-development-like-manufacturing': 6, 'https://www.globalapptesting.com/blog/topic/improving-quality/page/4': 1, 'https://www.globalapptesting.com/blog/the-real-cost-behind-missing-bugs': 4, 'https://www.globalapptesting.com/blog/best-way-work-qa-agency': 3, 'https://www.globalapptesting.com/blog/crowdsourced-testing': 5, 'https://www.globalapptesting.com/blog/topic/improving-quality/page/0': 1, 'https://www.globalapptesting.com/qaops-playbook/how-to-build-a-culture-of-developing-quality-products': 3,
            'https://www.globalapptesting.com/company/careers': 5, 'https://www.globalapptesting.com/company/events': 1, 'https://www.globalapptesting.com/product/test-case-execution': 1, 'https://www.globalapptesting.com/products/mobile-app-testing': 7, 'https://www.globalapptesting.com//www.globalapptesting.com/contact-sales': 1, 'https://www.globalapptesting.com/blog/does-your-qa-save-lives-upcoming-webinar': 3, 'https://www.globalapptesting.com/blog/9-essential-continuous-testing-reads-for-anyone-in-qa': 4, 'https://www.globalapptesting.com/blog/does-good-qa-contribute-to-good-cybersecurity': 5, 'https://www.globalapptesting.com/blog/how-to-adjust-qa-for-continuous-integration': 2,
            'https://www.globalapptesting.com/blog/the-ultimate-guide-to-software-testing-how': 2, 'https://www.globalapptesting.com//go-globalapptesting-com.sandbox.hs-sites.com/speak-to-us': 2, 'https://www.globalapptesting.com/blog/automated-qa-testing': 5, 'https://www.globalapptesting.com/blog/time-management-techniques': 4, 'https://www.globalapptesting.com/blog/is-crowdsourced-testing-outsourcing': 5, 'https://www.globalapptesting.com/blog/author/wojtek-olearczyk': 1, 'https://www.globalapptesting.com/blog/author/wojtek-olearczyk/page/0': 2, 'https://www.globalapptesting.com/blog/outsourcing-software-testing-vs-crowdsourcing-whats-the-difference': 3, 'https://www.globalapptesting.com/blog/software-testing-methodologies-': 9,
            'https://www.globalapptesting.com/blog/what-is-automation-testing': 9, 'https://www.globalapptesting.com/localization-testing': 3, 'https://www.globalapptesting.com/blog/whats-slowing-down-your-release-cycle': 6, 'https://www.globalapptesting.com/blog/when-should-you-automate-your-software-testing': 5, 'https://www.globalapptesting.com/blog/author/nishi-grover-garg': 1, 'https://www.globalapptesting.com/blog/author/nishi-grover-garg/page/0': 2, 'https://www.globalapptesting.com/blog/why-is-testing-important-for-tech-startups': 4, 'https://www.globalapptesting.com/blog/upgrade-your-qa-without-breaking-the-bank': 4, 'https://www.globalapptesting.com/blog/how-to-build-a-mobile-app-that-customers-love': 5,
            'https://www.globalapptesting.com/blog/testing-in-agile': 4, 'https://www.globalapptesting.com/demo-request-typ': 2, 'https://www.globalapptesting.com/blog/author/sasha-nagarajah': 3, 'https://www.globalapptesting.com/blog/author/sasha-nagarajah/page/0': 2, 'https://www.globalapptesting.com/products': 1, 'https://www.globalapptesting.com/blog/the-role-of-qa-in-your-sdlc-process': 2, 'https://www.globalapptesting.com//go.globalapptesting.com/industry/proptech': 1, 'https://www.globalapptesting.com//go.globalapptesting.com/webinar-dont-ignore-qa': 1, 'https://www.globalapptesting.com/blog/when-bugs-take-over-and-how-to-stop-them': 7, 'https://www.globalapptesting.com/blog/adjusting-your-tech-budget-to-survive-uncertain-times': 3,
            'https://www.globalapptesting.com/blog/how-to-achieve-5-star-app-reviews': 3, 'https://www.globalapptesting.com/blog/achieving-diversity-in-software-testing': 3, 'https://www.globalapptesting.com/blog/app-users-today-have-no-time-for-poor-quality': 3, 'https://www.globalapptesting.com/blog/app-retention': 2, 'https://www.globalapptesting.com/blog/dealing-with-unexpected-delays-in-your-release-cycle': 3, 'https://www.globalapptesting.com/blog/author/alister-esam': 2, 'https://www.globalapptesting.com/blog/author/alister-esam/page/0': 2, 'https://www.globalapptesting.com/blog/the-software-bugs-affecting-young-drivers': 2, 'https://www.globalapptesting.com//go.globalapptesting.com/exploratory-testing-enterprise-guide': 1,
            'https://www.globalapptesting.com/blog/author/melanie-bernard': 8, 'https://www.globalapptesting.com/blog/testing-trends-breakfast-of-champions': 3, 'https://www.globalapptesting.com/blog/author/melanie-bernard/page/0': 2, 'https://www.globalapptesting.com/blog/what-is-continuous-integration': 3, 'https://www.globalapptesting.com/blog/topic/qaops/page/0': 1, 'https://www.globalapptesting.com/blog/author/cynthia-lin': 2, 'https://www.globalapptesting.com/blog/author/cynthia-lin/page/0': 2, 'https://www.globalapptesting.com/blog/testing-in-production': 2, 'https://www.globalapptesting.com/blog/the-remote-testing-checklist': 4, 'https://www.globalapptesting.com/blog/remote-testing-making-the-switch': 2,
            'https://www.globalapptesting.com//go.globalapptesting.com/ebook-ultimate-guide-to-crowdsourced-testing?hsCtaTracking=01c742d5-a6d1-4494-b7da-61ec123982e1%7Cfa58782c-fd94-4276-b957-f4d73210fc39': 1, 'https://www.globalapptesting.com/blog/author/jeremy-palmer': 1, 'https://www.globalapptesting.com/blog/author/jeremy-palmer/page/0': 2, 'https://www.globalapptesting.com/blog/author/nick-roberts/page/1': 2, 'https://www.globalapptesting.com/blog/author/nick-roberts/page/3': 1, 'https://www.globalapptesting.com/blog/author/nick-roberts/page/0': 1, 'https://www.globalapptesting.com/blog/benefits-of-on-demand-qa': 2, 'https://www.globalapptesting.com/blog/4-alternatives-to-hiring-internal-qa': 2,
            'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/1': 2, 'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/3': 2, 'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/4': 2, 'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/5': 1, 'https://www.globalapptesting.com/blog/author/fahim-sachedina/page/0': 1, 'https://www.globalapptesting.com/blog/business-continuity-planning-software-release': 2, 'https://www.globalapptesting.com/blog/the-ultimate-qa-testing-handbook-highlights': 1, 'https://www.globalapptesting.com/blog/exploratory-testing-week-the-highlights': 1, 'https://www.globalapptesting.com/blog/page/1': 2, 'https://www.globalapptesting.com/blog/page/3': 2,
            'https://www.globalapptesting.com/blog/page/4': 2, 'https://www.globalapptesting.com/blog/apples-surprise-update-causes-bug-fears': 1, 'https://www.globalapptesting.com/blog/announcing-iso-27001-certification': 1, 'https://www.globalapptesting.com/blog/top-tech-blogs-to-read-in-2020': 1, 'https://www.globalapptesting.com/blog/page/5': 2, 'https://www.globalapptesting.com/blog/using-qa-to-seek-and-destroy-technical-debt': 1, 'https://www.globalapptesting.com/blog/why-your-releases-keep-getting-delayed-and-what-to-do-about-it': 1, 'https://www.globalapptesting.com/blog/page/6': 2, 'https://www.globalapptesting.com/blog/remote-tips-on-building-a-positive-company-culture': 1, 'https://www.globalapptesting.com/blog/page/7': 2,
            'https://www.globalapptesting.com/blog/scale-your-qa-team-globally': 1, 'https://www.globalapptesting.com/blog/how-to-improve-communication': 1, 'https://www.globalapptesting.com/blog/page/8': 2, 'https://www.globalapptesting.com/blog/spooky-software-bugs': 1, 'https://www.globalapptesting.com/blog/page/9': 2, 'https://www.globalapptesting.com/blog/page/10': 2, 'https://www.globalapptesting.com/blog/page/11': 2, 'https://www.globalapptesting.com/blog/page/12': 2, 'https://www.globalapptesting.com/blog/page/13': 2, 'https://www.globalapptesting.com/blog/page/14': 2, 'https://www.globalapptesting.com/blog/page/15': 1, 'https://www.globalapptesting.com/blog/page/0': 1, 'https://www.globalapptesting.com/engineering/author/nick-roberts': 2,
            'https://www.globalapptesting.com/blog/topic/ruby/page/0': 2, 'https://www.globalapptesting.com/engineering/author/damian-mamla': 1, 'https://www.globalapptesting.com/engineering/author/adam-mazur': 1, 'https://www.globalapptesting.com/blog/topic/data-science/page/0': 2, 'https://www.globalapptesting.com/engineering/author/tomasz-wrona': 1, 'https://www.globalapptesting.com/engineering/author/tomasz-wrona/page/0': 2, 'https://www.globalapptesting.com/engineering/author/jakub-niwa': 1, 'https://www.globalapptesting.com/engineering/author/jakub-niwa/page/0': 2, 'https://www.globalapptesting.com/engineering/author/jan-jędrychowski': 1, 'https://www.globalapptesting.com/engineering/author/jan-jędrychowski/page/0': 2,
            'https://www.globalapptesting.com/engineering/tag/increasing-speed/page/0': 2, 'https://www.globalapptesting.com/engineering/tag/data-science/page/0': 2, 'https://www.globalapptesting.com/engineering/tag/inside-gat/page/0': 2, 'https://www.globalapptesting.com/engineering/tag/ruby/page/0': 2, 'https://www.globalapptesting.com/engineering/tag/engineering/page/0': 2, 'https://www.globalapptesting.com/engineering/author/nick-roberts/page/0': 2, 'https://www.globalapptesting.com/engineering/author/piotr-brych': 2, 'https://www.globalapptesting.com/engineering/author/piotr-brych/page/0': 2, 'https://www.globalapptesting.com/engineering/author/wojtek-olearczyk': 1, 'https://www.globalapptesting.com/engineering/author/wojtek-olearczyk/page/0': 2,
            'https://www.globalapptesting.com/engineering/author/michal-forys': 1, 'https://www.globalapptesting.com/engineering/author/michal-forys/page/0': 2, 'https://www.globalapptesting.com/engineering/author/adam-mazur/page/0': 2, 'https://www.globalapptesting.com/engineering/author/damian-mamla/page/0': 2, 'https://www.globalapptesting.com/engineering/page/1': 2, 'https://www.globalapptesting.com/engineering/page/0': 1}


def test_get_links_from_web_page_no_url(web_parser):
    '''
    Test ArgumentNotProvided exception.
    '''

    with pytest.raises(ArgumentNotProvided):
        web_parser.perform_get_request()


def test_get_links_from_web_page(web_parser: WebpageParser, build_path: Callable[[], str]):
    '''
    Test if the obtained links are correct - with minimal attempts.
    '''

    link_10 = '<a aria-expanded="false" aria-haspopup="true" data-hs-event-102002560="1" data-hs-event-190178346="1" data-hs-event-205950610="1" data-hs-event-43945764="1" href="https://www.globalapptesting.com/solutions" role="menuitem">Solutions</a>'
    last_link = '<a href="https://go.globalapptesting.com/speak-to-us" role="menuitem">Speak to Us</a>'
    links_len = 167

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)

        assert str(links[10]) == link_10
        assert str(links[-1]) == last_link
        assert len(links) == links_len


def test_extract_hrefs_invalid_type_for_links(web_parser: WebpageParser, root_link: str):
    '''
    Test the exception when invalid data types for links are provided.
    '''

    with pytest.raises(ValueError):
        web_parser.extract_hrefs(links=1)


def test_extract_hrefs_empty_links_list(web_parser: WebpageParser, root_link: str):
    '''
    Test when the links list is empty - returns an dict with empty Counter objects.
    '''

    hrefs = web_parser.extract_hrefs(links=[])

    assert 'internal_links' in hrefs
    assert 'external_links' in hrefs
    assert 'dead_links' in hrefs
    assert 'phone_links' in hrefs
    assert 'email_links' in hrefs

    assert not hrefs['internal_links']
    assert not hrefs['external_links']
    assert not hrefs['dead_links']
    assert not hrefs['phone_links']
    assert not hrefs['email_links']


def test_extract_hrefs(web_parser: WebpageParser, build_path: Callable[[], str], root_link: str):
    '''
    Test the correct extraction of hrefs.
    '''

    internal_href_key = 'https://www.globalapptesting.com/product'
    external_href_key = 'https://www.leadingqualitybook.com/'

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)
        hrefs = web_parser.extract_hrefs(links=links)

        assert 'internal_links' in hrefs
        assert 'external_links' in hrefs
        assert 'dead_links' in hrefs
        assert 'phone_links' in hrefs
        assert 'email_links' in hrefs

        assert hrefs['internal_links'].get(internal_href_key, 0) == 9
        assert hrefs['external_links'].get(external_href_key, 0) == 3
        assert not hrefs['dead_links']
        assert not hrefs['phone_links']
        assert not hrefs['email_links']


def test_extract_links_from_counter_invalid_obj_type(web_parser: WebpageParser):
    '''
    Test the exceptin when the argument counter_obj is not of type Counter.
    '''

    with pytest.raises(ValueError):
        web_parser.extract_links_from_counter(counter_obj=[])


def test_extract_links_from_counter_empty_object(web_parser: WebpageParser):
    '''
    Test the exceptin when the argument counter_obj is empty - returns an empty list.
    '''

    links = web_parser.extract_links_from_counter(counter_obj=Counter())
    assert not links


def test_extract_links_from_counter(web_parser: WebpageParser, build_path: Callable[[], str], root_link: str):
    '''
    Test the correct extraction of links from the Counter object.
    '''

    file_path = build_path('global_test_app', 'html')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        links = web_parser.get_links_from_web_page(fhandle)
        hrefs = web_parser.extract_hrefs(links=links)
        local_links_extraction = [link for link,
                                  _ in hrefs['internal_links'].items()]

        extracted_internal_links = web_parser.extract_links_from_counter(
            hrefs['internal_links'])
        assert extracted_internal_links == local_links_extraction


'''
This test is commented because the current
implementation will query the real website
and it takes too much time to finish.
'''
# def test_build_dict_map(web_parser: WebpageParser, root_link: str):
#     '''
#     Test the correct generation of dict map.
#     '''

#     actual_obj_map = web_parser.build_dict_map()

#     response = web_parser.perform_get_request(url=root_link)
#     links = web_parser.get_links_from_web_page(web_page=response)
#     hrefs = web_parser.extract_hrefs(links=links, root=root_link)
#     extracted_internal_links = web_parser.extract_links_from_counter(
#         hrefs['internal_links'])

#     expected_map = {root_link: hrefs}
#     for url in extracted_internal_links:
#         response = web_parser.perform_get_request(url=root_link)
#         page_links = web_parser.get_links_from_web_page(web_page=response)
#         counter_links = web_parser.extract_hrefs(links=page_links, root=url)
#         expected_map[url] = counter_links

#     assert type(expected_map) == type(actual_obj_map)
#     for (key_map, value_map), (key_obj_map, value_obj_map) in zip(expected_map[root_link].items(), actual_obj_map[root_link].items()):
#         assert key_map == key_obj_map
#         assert value_map == value_obj_map


def test_convert_counters_to_graph_edges_tuples(web_parser_without_root: WebpageParser, temp_map_dict: dict, graph_edges: list):
    '''
    Test convertion of Counter objects into tuples that represent the edges of a graph.

    '''

    web_parser_without_root.map_dict = temp_map_dict
    obtained_graph_dict = web_parser_without_root.convert_counters_to_graph_edges()

    for expected_tuple, obtained_tuple in zip(graph_edges, obtained_graph_dict['https://www.globalapptesting.com/']):
        # the expected tuples contain \n added by vscode beacause of auto formating, for this reason the comparision is done by elements
        for exp_element, obt_element in zip(expected_tuple, obtained_tuple):
            assert exp_element == obt_element


def test_private_write_to_file(web_parser_without_root: WebpageParser, build_path: Callable[[], str], small_map_sample: dict):
    '''
    Test the writing dict object to the json file.
    '''

    file_name = 'test_file'
    file_path = build_path(file_name)
    web_parser_without_root._WebpageParser__write_to_file(data=small_map_sample,
                                                          file_name=file_path)

    with open(file=build_path(file_name, 'json'), mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert small_map_sample == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_write_map_dict_to_json_file(web_parser_without_root: WebpageParser, build_path: Callable[[], str], small_map_sample: dict):
    '''
    Test the writing map_dict object to the json file.
    '''

    web_parser_without_root.map_dict = small_map_sample
    file_name = 'test_map_dict'
    file_path = build_path(file_name)
    web_parser_without_root.write_map_dict_to_json_file(file_name=file_path)
    with open(file=build_path(file_name, 'json'), mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert small_map_sample == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_write_graph_dict_to_json_file(web_parser_without_root: WebpageParser, expected_json, build_path: Callable[[], str], temp_graph_dict: dict):
    '''
    Test the writing graph_dict object to the json file.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict
    web_parser_without_root.write_graph_dict_to_json_file(
        file_name=build_path('test_graph_dict'))

    file_name = 'test_graph_dict'
    file_path = build_path(file_name, 'json')
    with open(file=file_path, mode='r', encoding='utf8') as fhandle:
        try:
            obtained_json = json.load(fhandle)
            assert expected_json == obtained_json
        except Exception as exc:
            print(
                f'Exception occured when trying to read from the json file with name={file_name}: {exc}')


def test_private_load_from_json(web_parser_without_root: WebpageParser, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of dictionary from json.
    '''

    file_name = 'test_load'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = web_parser_without_root._WebpageParser__load_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_load_map_dict_from_json(web_parser_without_root: WebpageParser, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of the map dictionary from json.
    '''

    file_name = 'test_load_map_dict'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = web_parser_without_root.load_map_dict_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_load_graph_dict_from_json(web_parser_without_root: WebpageParser, build_path: Callable[[], str], expected_json_sample: json, write_to_json_file: Callable[[str, ], None]):
    '''
    Test the correct loading of the graph dictionary from json.
    '''

    file_name = 'test_load_graph_dict'
    write_to_json_file(file_name, expected_json_sample)
    obtained_json = web_parser_without_root.load_graph_dict_from_json(
        file_name=build_path(file_name))
    assert expected_json_sample == obtained_json


def test_get_link_info(web_parser_without_root: WebpageParser,  temp_map_dict: dict):
    '''
    Test statistic info of a given link.
    '''

    web_parser_without_root.map_dict = temp_map_dict
    expected_dict = {'internal_links': 5,
                     'external_links': 6,
                     'dead_links': 0,
                     'phone_links': 0,
                     'email_links': 0,
                     'file_links': 0,
                     'HTTP_STATUS': 200}
    obtained_dict = web_parser_without_root.get_link_info(
        'https://www.globalapptesting.com/')

    assert expected_dict == obtained_dict


def test_get_webpage_statistics(web_parser_without_root: WebpageParser, build_path: Callable[[], str]):
    '''
    Validate the webpage statistic values and format.
    '''

    web_parser_without_root.load_map_dict_from_json(
        file_name=build_path('test_map_dict_full'))
    web_parser_without_root.load_graph_dict_from_json(
        file_name=build_path('test_graph_dict_full'))
    expected_statistic = '\nGeneral information about                  \n\nTotal web pages found (unique links):      361\nHTTP 200:                                  354\nHTTP 404:                                  7\n\nTotal internal links (non-unique links):   17409\nDistance between the most distant pages:   379\n\nTotal external links:                      5207\nTotal dead links:                          86\nTotal phone links:                         25\nTotal email links:                         183\nTotal file links:                          36\n\nAverage number of internal links per page: 48\nAverage number of external links per page: 14\nAverage size (in bytes) per page:          97343'
    obtained_statistic = web_parser_without_root.get_webpage_statistics()
    assert expected_statistic == obtained_statistic[:657]


def test_get_link_status_code(web_parser_without_root: WebpageParser,  temp_map_dict: dict):
    '''
    Check if the returned HTTP status code is correct.
    '''

    web_parser_without_root.map_dict = temp_map_dict
    obtained_status_code = web_parser_without_root.get_link_status_code(
        'https://www.globalapptesting.com/')
    assert 200 == obtained_status_code


def test_get_pages_with_min_max_links(web_parser_without_root: WebpageParser, temp_graph_dict_full: dict):
    '''
    Validate integrity of returned dictionary.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict_full
    obtained_dict = web_parser_without_root.get_pages_with_min_max_links()

    assert 'maximum_incoming_links' in obtained_dict
    assert 'minimum_incoming_links' in obtained_dict
    assert obtained_dict['maximum_incoming_links']['incoming_links_count'] == 361
    assert obtained_dict['minimum_incoming_links']['incoming_links_count'] == 1
    assert len(obtained_dict['maximum_incoming_links']
               ['links']) == 3
    assert len(obtained_dict['minimum_incoming_links']
               ['links']) == 48


def test_count_incoming_links(web_parser_without_root: WebpageParser, temp_graph_dict_full: dict, expected_incoming_count_links: dict):
    '''
    Validate integrity of returned dictionary.
    '''

    web_parser_without_root.graph_dict = temp_graph_dict_full
    obtained_incoming_links_counter = web_parser_without_root.count_incoming_links()
    assert expected_incoming_count_links == obtained_incoming_links_counter


def test_get_longest_path(web_parser_without_root: WebpageParser, temp_graph_dict_full: dict):
    '''
    Check if the value of method get_lingest_path is equal to expected one.
    '''
    web_parser_without_root.graph_dict = temp_graph_dict_full
    obtained_longest_path = web_parser_without_root.get_longest_path()
    expected_longest_path = 379
    assert expected_longest_path == obtained_longest_path
