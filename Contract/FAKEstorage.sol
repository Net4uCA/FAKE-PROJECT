// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

/* This contract is the first part of the describer of the FAKE system.
It is compiled to create the main structure that compose a News on the entire System.
General structure follows the schema realised by the FAKE project team
and available with the JSON schema validator in *URL OF THE WEBSITE (GIT I SUPPOSE)*
*/

contract FAKEstorage {
    /* Contract where is defined the news structure and its main functions to operate with */

    address private owner;

    struct topic {
        string level1;
        string level2;
    }

    struct message {
        uint256 value;
        uint256 typos;
        string word_freq;
    }

    struct fact {
        string value;
        string[] bow;
    }

    struct context {
        string value;
        uint256 n_ads;
        uint256 n_ref;
        string text_title;
        string author;
    }

    struct Article {
        uint256 Id;
        string URL;
        string Source;
        uint256 Datatime;
        topic Topic;
        bool Social;
        message Message;
        fact Fact;
        context Context;
        string Feedback;
    }

    struct Source {
        string name;
        Article[] articles;
    }

    struct Topic {
        string topic;
        Article[] articles;
    }

    constructor() {
        owner = msg.sender;
    }

    uint256 index = 1;
    bool check;
    string nota;

    mapping(uint256 => Article) articles;
    mapping(string => Article) news;
    mapping(string => Source) sources;
    mapping(string => Topic) topic_articles;

    mapping(uint256 => mapping(string => Article)) context_value;

    function store_article(
        string memory _URL,
        string memory _Source,
        string memory _Feedback,
        string memory _level1,
        string memory _level2
    ) public {
        // e.g. "http://www.repubblica.it/notizie/sport/golf/molinari-campione-del-mondo","www.repubblica.it","0.89","sport","golf"
        // e.g. "http://www.ruttosport.it/news/sport/calcio/messi-al-cagliari","www.ruttosport.it","0.2","sport","calcio"
        // e.g. "http://www.ruttosport.it/news/sport/basket/lebron-james-si-da-all-ippica","www.ruttosport.it","0.35","sport","basket"
        // e.g. "http://www.repubblica.it/notizie/politica/mattarella-nominato-presidente","www.repubblica.it","0.89","politica"

        if (index > 1) {
            for (uint256 i = 1; i <= index; i++) {
                if (
                    keccak256(bytes(articles[i].URL)) == keccak256(bytes(_URL))
                ) {
                    check = false;
                    require(check, "News is already in the system");
                } else {
                    check = true;
                }
            }
        }

        articles[index].Id = index;
        articles[index].Datatime = block.timestamp;
        articles[index].URL = _URL;
        articles[index].Source = _Source;
        articles[index].Feedback = _Feedback;
        articles[index].Topic.level1 = _level1;
        articles[index].Topic.level2 = _level2;

        news[_URL] = articles[index];

        if (
            keccak256(bytes(sources[_Source].name)) == keccak256(bytes(_Source))
        ) {
            sources[_Source].articles.push(articles[index]);
        } else {
            sources[_Source].name = _Source;
            sources[_Source].articles.push(articles[index]);
        }

        if (
            keccak256(bytes(topic_articles[_level1].topic)) ==
            keccak256(bytes(_level1))
        ) {
            topic_articles[_level1].articles.push(articles[index]);
        } else {
            topic_articles[_level1].topic = _level1;
            topic_articles[_level1].articles.push(articles[index]);
        }

        index++;
    }

    function get_article_by_id(uint256 _Id)
        public
        view
        returns (Article memory)
    {
        return articles[_Id];
    }

    function get_article_by_url(string memory _URL)
        public
        view
        returns (Article memory)
    {
        return news[_URL];
    }

    function get_articles_of_source(string memory _Source_name)
        public
        view
        returns (Article[] memory)
    {
        return sources[_Source_name].articles;
    }

    function get_articles_of_same_topic(string memory _topic)
        public
        view
        returns (Article[] memory)
    {
        return topic_articles[_topic].articles;
    }

    function get_lastN_source_articles(string memory _Source, uint256 n)
        public
        view
        returns (Article[] memory)
    {
        uint256 arr_length = sources[_Source].articles.length;
        Article[] memory article_list = new Article[](arr_length);
        if (n > arr_length) {
            n = arr_length;
        }
        uint256 idx = arr_length - n;
        uint256 art_ind = 0;
        for (uint256 i = arr_length; i > idx; i--) {
            Article memory article = sources[_Source].articles[i - 1];
            article_list[art_ind] = article;
            art_ind += 1;
        }
        return article_list;
    }
}
