# MoodleFetcher

## What is this project?
So, basically, it's a pet project that helps me get grades, deadlines, predicted grades and statistics from my courses in Moodle.
### But why I don't want to use Moodle? 
This platform is not convenient for me at all. You need to log in every time you want to see your deadlines and grades (if they are available), and even if you are logged in, it logs you out automatically after some time.

## Facilities
- Easy-to-use bot in Telegram
- Moodle authorization and data fetching
- Syllabus parsing
- Deadline notifications (? Future)
- Course grade analysis via graphs and statistics. (Not finished)
- Grade prediction based on current grades and assessment weights. (Not finished)
- Data storing in DB (? Future)

> [!NOTE]
> Project is not finished yet. So there might be some changes

## Used technologies 

```
Programming language: Python 3.13+
Data fetching: Selenium (Web Scraping, ~Moodle API~)
Syllabus: pdfplumber
Bot platform: Telegram (Telegram API)
DB: (?)
Statistics: matplotlib, numpy (Not finished)
```

## Architecture

> [!NOTE]
> I don't have experience in building architectures, so it might be wrong

[ User ]
  - v
[ Telegram Bot ]
  - v           \
[ DB ]           \
    ^             v
    -----------[ App ]  ----> [ Syllabus Parser ]
                 /     ^              v
                /       \ --- [Statistics / Analyzer]
               v                     ^
        [ Grade Fetcher ]  -----------