https://fedora-book-app-66de4d4087a8.herokuapp.com/
https://github.com/Apostle01/Fedora_book_app.git

# Fedora_book_app

Fedora_book_app was created as my third milestone project, built using a Flask framework alongside PostgreSQL.

![fedora-book-app. Screenshot of website](docs/am-i-responsive.png)

[View Fedora_book_app on Heroku](https://fedora-book-app-66de4d4087a8.herokuapp.com/)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Apostle01/Fedora_book_app)
![GitHub language count](https://img.shields.io/github/languages/count/Apostle01/Fedora_book_app)
![GitHub top language](https://img.shields.io/github/languages/top/Apostle01/Fedora_book_app color=red)


## CONTENTS

- [User Experience (UX)](#User-Experience-UX)

  - [User Stories](#User-Stories)

- [Design](#Design)

  - [Colour Scheme](#Colour-Scheme)
  - [Typography](#Typography)
  - [Imagery](#Imagery)
  - [Wireframes](#Wireframes)
  - [Database Design](#database-design)
  
- [Features](#Features)
    - [Web Pages](#web-pages)
    - [Accessibility](#Accessibility)

- [Technologies Used](#Technologies-Used)
  - [Languages Used](#Languages-Used)
  - [Frameworks, Libraries & Programs Used](#frameworks-libraries-and-programs-used)

- [Deployment and Local Development](#deployment--local-development)  
    - [Local Development](#Local-Development)
    - [Remote Deployment](#remote-deployment-heroku)
   

- [Testing](#Testing)

  - [Solved Bugs](#Solved-Bugs)
  - [Known Bugs](#Known-Bugs)

- [Credits](#Credits)
  - [Code Used](#Code-Used)
  - [Media](#Media)
  - [Acknowledgments](#Acknowledgments)

---

## User Experience (UX)
Purpose
The primary purpose of Apostle01/Fedora_book_app is to create an engaging and user-friendly platform where book enthusiasts can share and discover book reviews. This website is designed to serve as a comprehensive resource for individuals looking to gain insights into various books through the opinions and experiences of other readers. By leveraging the TMDB API, the site provides up-to-date information on a wide range of books, enhancing the user's ability to search for and review books.

Why The Site is Needed
Centralized community for book enthusiasts - there is a need for a dedicated space that brings together a community of book lovers.
User-generated content - Fedora Book App represents the reviews of everyday readers, offering a diverse range of perspectives. Existing sites often rely on professional critics.
Accessibility and ease of use - some existing sites can be overwhelming or difficult to navigate. Fedora Book App is designed with a user-friendly interface that makes it easy for anyone to search for books, read reviews, and leave their own.
Customization and personalization - Fedora Book App allows the user to manage their reviews.

Security Features
Authentication and Authorization - Users can register and log in with password hashing to protect user credentials. Users can only modify or delete their own reviews. If another user tries to access a different user's review area via a URL, they are met with a 403 page.
Why Fedora Book App?
TMDB API - By using TMDB, users have access to a vast and up-to-date database of books.
Tailored Experience - Giving the user the ability to view their review history, delete, and update reviews provides a more personalized approach in comparison to similar platforms.
Target Audience
Book Enthusiasts: Individuals who love reading books and are interested in sharing their opinions and reading reviews from like-minded people.
General Audience: People who want to read reviews before deciding to read a book.
User Stories
First Time Visitor Goals
Register for an account.
Search for books.
Understand what the site is for and easily navigate their way around.
Returning Visitor Goals
Log into a created account.
Create, edit, and delete my reviews.
Read other users' reviews.
Frequent Visitor Goals
Log into a created account.
Create, edit, and delete my reviews.
Read other users' reviews.
Design
Colour Scheme

The red, white, and black color scheme is bold and modern, offering a high-contrast, visually engaging design. This theme combines the elegance of black, the cleanliness of white, and the vibrant energy of red to create an impactful user experience. The coolors website was used to develop the color palette.

Typography
Google Fonts was used for the following fonts:

Barrio is used for the main Fedora Book App logo, nav links, and footer text.

Helvetica is used for the remaining text across the website.
Imagery
All images on the webpage were taken from TMDB. I have credited these in the credits section.

Wireframes
Wireframes were created for mobile, tablet, and desktop using Balsamiq.

Desktop Wireframes

Tablet Wireframes

Mobile Wireframes

Database Design
Fedora Book App is based on a relational database. The database is made up of 3 tables: User, Book, and Review tables. The tables are related via their primary and foreign keys in addition to the backrefs, which made querying the database easier.

The backref command reviews = db.relationship( 'Review', backref='user') on the User table creates a virtual column on the Review table called user, making it easier to query the database. For example, you can access the reviews from the User table using User.reviews while also accessing a user from the Reviews table using Review.user. This approach has been beneficial when displaying reviews linked to different users.

The relationships between the tables are as follows:

User to Review: One-to-Many. One user can write many reviews. This relationship is defined using db.relationship in the User model and db.ForeignKey in the Review model.
Book to Review: One-to-Many. One book can have many reviews. This relationship is defined using db.relationship in the Book model and db.ForeignKey in the Review model.

Features
The website consists of 12 pages, which are extended from a base template.

Home Page
Login Page
Sign Up Page
Search Page
Search Results Page
Add Review Page
Edit Review Page
Delete Review (Modal)
My Reviews Page
Book Reviews Page
404 Page
500 Page
403 Page

All 12 pages have the following elements in common:
Navbar - The navbar is present on all pages throughout the website. This allows each user to navigate their way around the website with ease. It consists of the Fedora Book App logo on the left-hand side and the nav links on the right. The nav links have an active attribute on them and are highlighted in red to show the user which page they're on. Certain nav links are only visible if the user is logged in.
User Logged Out

User Logged In

Nav Links
The nav links are highlighted in red, indicating which page the user is on.
Footer
Footer - The footer is also present on each webpage and has links to Fedora Book App's social media pages.

Web Pages
Home Page

The homepage introduces the user to the website and also shows the top 12 trending books of the week. The signup and login buttons are only visible if the user is not logged in.
Sign Up Page

The signup page allows the user to create an account for Fedora Book App. An account is required in order to search for books, leave reviews, edit, and delete reviews.
Login Page

The login page allows the user to log in to the website.
Book Reviews Page

The book reviews page shows reviews posted by all users. This is a read-only page.
My Reviews Page

The My Reviews page displays all the reviews posted by the logged-in user. From here, the user can modify existing reviews or delete their review. Only the original poster can modify or delete their own reviews.
Search Books Page

The search books page allows a user to search for a book using the TMDB database.
Search Results Page

The search results page displays all of the books related to the search query. For the books that do not have an image, I opted to use a stock image from TMDB rather than not displaying an image. The user can simply click on the image to be taken to the review form.
Leave A Review Page

This page allows the user to create a review of their chosen book. Once submitted, the review is stored in the database.
Edit A Review Page

The edit review page allows a user to edit a review they have previously created. The edit button is only visible to the user who created the review. The code also checks to see if the logged-in user matches the user ID of the person who posted the review.
Delete A Review Page

The delete review page allows a user to delete a review they have previously created. The delete button is only visible to the user who created the review. The code also checks to see if the logged-in user matches the user ID of the person who posted the review. A modal is then displayed to confirm whether the user wants to delete the review.
404 Page

The user is directed to the 404 page if a page cannot be found.
500 Page

The user is directed to the 500 page if there is an internal server error.
403 Page
![403]








