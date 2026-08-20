# CourseHub v1 Product Brief

**Status:** Approved  
**Created:** 2026-08-19  
**Author:** Gokul  
**Purpose:** Full-stack learning and portfolio project

## Executive Summary

CourseHub is a local-first full-stack course listing application. Learners can discover, search, filter, view, and freely enroll in courses, then track them in My Learning. Admins manage the catalog through a React dashboard. The project demonstrates a coherent React + Django/DRF + MySQL stack with JWT authentication, role-based access control, relational modeling, and local media uploads.

CourseHub is inspired by the browsing experience of modern learning platforms such as Altalya, but it will have its own visual identity. It is intentionally scoped as a portfolio and learning project rather than a commercial launch.

## Users and Experiences

| Experience | Users | Capabilities |
|---|---|---|
| Learner UI | Registered learners | Register, log in, browse, search, filter, view course details, enroll for free, and view My Learning |
| Admin dashboard | Admin users | Manage courses, categories, instructors, course images, instructor photos, and enrollments |
| REST API | Both roles | Provides application data and enforces JWT authentication and role-based permissions |

The React admin dashboard is the primary admin interface. Django `/admin` remains available only as a development/testing shortcut.

## Scope

### In scope

- Learner registration and login
- JWT access and refresh tokens
- Role-based learner/admin access
- Course card-grid browsing
- Search by course title and description
- Category filtering
- Course details: image, title, full description, displayed price, instructor, and category
- Free enrollment; prices are display-only in v1
- My Learning enrollment view
- Admin CRUD for courses, categories, and reusable instructor profiles
- Course image and instructor photo uploads stored on the local Django filesystem
- Admin enrollment views, including enrolled learners per course
- MySQL persistence
- React learner and admin interfaces
- Django REST Framework API
- Complete local setup README

### Out of scope

- Payments or checkout
- Deployment or live URL
- Cloud image storage
- Instructor-name search
- Multiple categories per course
- Reviews, ratings, wishlists, video lessons, analytics, or instructor self-service

## Data Model

The v1 domain includes users, courses, categories, instructors, and enrollments.

- Each course has exactly one category.
- Each course references one reusable instructor profile.
- Instructor profiles include name, bio, and optional photo.
- Courses include title, description, display price, image, category, and instructor.
- Enrollments connect learners to courses and support My Learning and admin enrollment views.

## Technical Decisions

- **Frontend:** React
- **Backend:** Python, Django, Django REST Framework
- **Database:** MySQL
- **Authentication:** `djangorestframework-simplejwt` with access and refresh tokens
- **Authorization:** Role-based permissions enforced by the API and reflected in the UI
- **Media:** Local filesystem via Django `MEDIA_ROOT`
- **Environment:** Local development only for v1

## Success Criteria

CourseHub v1 is complete when learner and admin flows work end-to-end, learners cannot access admin operations, JWT and role permissions are enforced at the API, the relational model supports reusable instructors and single-category courses, local media uploads work, and a beginner-friendly README documents complete setup for React, Django/DRF, and MySQL.

## Vision

In v2, CourseHub may be deployed with a live demo, migrate media to Cloudinary or S3, and optionally add payments. Future iterations may expand discovery and learning features only after the v1 foundation is complete.
