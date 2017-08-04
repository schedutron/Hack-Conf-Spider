# Hack-Conf-Spiders
## Spiders for Hackathons and Conferences

Here's a quick demo on conference scraping - In your terminal, do:

`scrapy crawl papercall -o info.json`

In place of `papercall`, `oreilly`, `opensource`, `lanyrd` and `linuxfoundation` can also be used.
(Currently only scraping from [papercall.io](http://papercall.io),  [oreilly.com](https://www.oreilly.com/conferences/), [opensource.com](https://opensource.com/resources/conferences-and-events-monthly),
[lanyrd.com](http://lanyrd.com/topics/open-source) and
[linuxfoundation.org](http://events.linuxfoundation.org) has been implemented with Scrapy.)

This will create a "info.json" file in your working directory. Here's a sample of it's contents (formatted for better readability):
```
[
    {
        "title": "Bristol JS",
        "description": "Offers travel assistance; We're always on the hunt for quality speakers. Since we run monthly talks we will be notifying sp...",
        "location": "Bristol, UK",
        "time": "Closes June 01, 2020 00:00 UTC",
        "tags": [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        "link": null,
        "source": "https://www.papercall.io"
    },
    {
        "title": "Ruby Novi Sad Meetup",
        "description": "Napi\u0161ite nekoliko re\u010denica o tome \u0161ta planirate da ispri\u010date i \u0161ta slu\u0161aoci mogu da o\u010dekuju da \u0107e...",
        "location": "Novi Sad, Serbia",
        "time": "Closes November 04, 2020 17:55 UTC",
        "tags": [
            "Ruby",
            "Ecosystem",
            "Rails"
        ],
        "link": "https://www.meetup.com/Ruby-Novi-Sad/",
        "source": "https://www.papercall.io"
    },
    {
        "title": "Docker Novi Sad Meetup",
        "description": "Napi\u0161ite nekoliko re\u010denica o tome \u0161ta planirate da ispri\u010date i \u0161ta slu\u0161aoci mogu da o\u010dekuju da \u0107e...",
        "location": "Novi Sad, Serbia",
        "time": "Closes April 18, 2021 14:44 UTC",
        "tags": [
            "Meetup",
            "Docker",
            "Devops"
        ],
        "link": "https://www.meetup.com/Docker-Novi-Sad/",
        "source": "https://www.papercall.io"
    },
    {
        "title": "CLE.py",
        "description": null,
        "location": null,
        "time": "Closes July 23, 2021 10:23 UTC",
        "tags": [
            "Web techonology",
            "Testing",
            "Advanced",
            "Security",
            "Intermediate",
            "Data science/analysis",
            "Packaging",
            "Python",
            "Beginner",
            "Data processing technology"
        ],
        "link": null,
        "source": "https://www.papercall.io"
    }
]
```
