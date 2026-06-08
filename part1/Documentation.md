# HBnB Evolution - Technical Documentation

## 1. Introduction

### Purpose

This document provides the technical design and architecture of the HBnB Evolution application. It serves as a blueprint for implementation by documenting the system architecture, business logic, and interactions between application components.

### Project Overview

HBnB Evolution is a simplified accommodation rental platform inspired by AirBnB. The system allows users to:

* Register and manage accounts
* Create and manage places
* Submit reviews
* Manage amenities
* Search and browse places

The application follows a layered architecture composed of:

* Presentation Layer
* Business Logic Layer
* Persistence Layer

Communication between layers is performed through a Facade pattern.

---

# 2. High-Level Architecture

## Overview

The system is divided into three layers:

### Presentation Layer

Responsibilities:

* REST API endpoints
* Request validation
* Response formatting
* User interaction

Components:

* API Controllers
* Services

### Business Logic Layer

Responsibilities:

* Business rules
* Entity management
* Domain validation

Components:

* User
* Place
* Review
* Amenity
* HBnBFacade

### Persistence Layer

Responsibilities:

* Data storage
* Data retrieval
* Database abstraction

Components:

* Repositories
* Database

---

## Facade Pattern

The HBnBFacade acts as a unified interface between the Presentation Layer and the Business Logic Layer.

Benefits:

* Reduced coupling
* Simplified API communication
* Easier maintenance
* Improved scalability

---

## High-Level Package Diagram

[Insert High-Level Package Diagram Image Here]

### Architecture Flow

User

↓

Presentation Layer

↓

HBnBFacade

↓

Business Logic Layer

↓

Persistence Layer

↓

Database

---

# 3. Business Logic Layer

## Overview

The Business Logic Layer contains all domain entities and business rules.

All entities inherit common properties from BaseEntity:

* UUID identifier
* Creation timestamp
* Update timestamp

---

## BaseEntity

### Attributes

* id : UUID
* created_at : datetime
* updated_at : datetime

### Methods

* save()
* update()
* delete()

---

## User Entity

### Attributes

* first_name
* last_name
* email
* password
* is_admin

### Methods

* register()
* update_profile()
* delete_user()

### Responsibilities

* Own places
* Submit reviews
* Manage profile

---

## Place Entity

### Attributes

* title
* description
* price
* latitude
* longitude

### Methods

* create_place()
* update_place()
* delete_place()
* add_amenity()
* remove_amenity()

### Responsibilities

* Store property information
* Associate amenities
* Receive reviews

---

## Review Entity

### Attributes

* rating
* comment

### Methods

* create_review()
* update_review()
* delete_review()

### Responsibilities

* Represent user feedback

---

## Amenity Entity

### Attributes

* name
* description

### Methods

* create_amenity()
* update_amenity()
* delete_amenity()

### Responsibilities

* Represent place features

---

## Relationships

### User → Place

One User owns many Places.

### User → Review

One User writes many Reviews.

### Place → Review

One Place receives many Reviews.

### Place ↔ Amenity

Many-to-Many relationship.

### BaseEntity → All Entities

Inheritance relationship.

---

## Business Logic Class Diagram

[Insert Detailed Class Diagram Image Here]

---

# 4. API Interaction Flow

This section describes the communication between layers during API execution.

---

## 4.1 User Registration

### Description

A new user creates an account.

### Flow

1. User sends registration request.
2. API validates request format.
3. Facade receives request.
4. User entity validates business rules.
5. Repository persists data.
6. Database stores user.
7. Success response returned.

### Diagram

[Insert User Registration Sequence Diagram]

---

## 4.2 Place Creation

### Description

An authenticated user creates a new property listing.

### Flow

1. User submits place information.
2. API forwards request.
3. Facade validates business rules.
4. Place repository stores record.
5. Database persists data.
6. Success response returned.

### Diagram

[Insert Place Creation Sequence Diagram]

---

## 4.3 Review Submission

### Description

A user submits a review for a place.

### Flow

1. User submits review.
2. API validates request.
3. Facade processes review.
4. Review repository stores data.
5. Database saves review.
6. Success response returned.

### Diagram

[Insert Review Submission Sequence Diagram]

---

## 4.4 Fetch Places

### Description

A user requests a list of places.

### Flow

1. User sends search request.
2. API forwards filters.
3. Facade requests places.
4. Repository queries database.
5. Results returned.
6. API responds with places list.

### Diagram

[Insert Fetch Places Sequence Diagram]

---

# 5. Design Decisions

## Layered Architecture

Advantages:

* Separation of concerns
* Easier maintenance
* Improved scalability
* Better testability

## Facade Pattern

Advantages:

* Simplifies interactions
* Reduces coupling
* Centralizes business operations

## Repository Pattern

Advantages:

* Database abstraction
* Easier future database changes
* Cleaner business layer

## UUID Identifiers

Advantages:

* Globally unique identifiers
* Better scalability
* Reduced collision risk

---

# 6. Conclusion

This technical document provides the architectural foundation for the HBnB Evolution project.

The package diagram defines the overall architecture, the class diagram specifies the business domain model, and the sequence diagrams illustrate how requests flow through the system.

Together, these diagrams provide a complete reference for the implementation phases of the project and ensure consistency across all components of the application.

