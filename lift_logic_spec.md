# Lift Logic – Web Application Specification

## 1. Application Overview

Lift Logic is a web application that generates personalised strength training programs based on a user’s one-rep max (1RM) for three core lifts:
- Squat
- Bench Press
- Deadlift

The system calculates training weights using percentage-based programming and presents structured workout routines. Users can also log their lifts and compare performance using a leaderboard.

---

## 2. Core Features

### 2.1 User Authentication
- Users must register and log in
- Registration requires:
  - Username
  - Password
  - 1RM for:
    - Squat
    - Bench Press
    - Deadlift

---

### 2.2 Homepage
- Displays three main options:
  - Squat
  - Bench Press
  - Deadlift
- Each option redirects to its respective program page

---

### 2.3 Strength Program System

Each lift has a predefined program (example: Smolov Jr).

#### Example Program (3-week cycle):
- Day 1: 6x6 at 70%
- Day 2: 7x5 at 75%
- Day 3: 8x4 at 80%
- Day 4: 10x3 at 85%

#### Calculation Logic:
- Weight = 1RM × Percentage
- Round result to nearest 2.5kg

#### Example:
- 1RM = 100kg
- 70% = 70kg

#### Progression:
- Weekly increase: +0 to +5kg depending on user feedback

---

### 2.4 Workout Page
- Displays:
  - Program structure (sets × reps)
  - Calculated weights
- Allows user to:
  - Log completed sets
  - Input actual weight and reps performed

---

### 2.5 Lift Logging
Users can log:
- Exercise
- Weight lifted
- Repetitions
- Date

System stores all entries in the database.

---

### 2.6 Feedback System
Based on user input:
- If easy → suggest increasing weight (+2.5kg to +5kg)
- If moderate → maintain weight
- If difficult → decrease weight

---

### 2.7 Profile Page
Displays:
- User’s lift history
- Logged sessions
- Progress over time

---

### 2.8 Leaderboard System

Users can submit:
- Bodyweight
- Exercise
- Weight lifted
- Repetitions
- Age

System calculates relative strength and ranks users.

---

## 3. Functional Requirements

- User must be able to register and log in
- User must input 1RM values
- System must calculate training weights using percentages
- System must round weights to nearest 2.5kg
- User must be able to:
  - Select a lift program
  - View workout routines
  - Log lifts
- System must store all user data
- Leaderboard must rank users based on performance

---

## 4. Non-Functional Requirements

- Secure authentication
- Responsive design (mobile + desktop)
- Database persistence
- Fast response time (< 2 seconds)

---

## 5. Pages and Routes

### Public Routes
- /login
- /sign-up

### Authenticated Routes
- /home
- /profile
- /leaderboard

### Workout Routes
- /workout/squat
- /workout/bench
- /workout/deadlift

---

## 6. Data Model

### User
- id
- username
- password
- squat_1rm
- bench_1rm
- deadlift_1rm

### LiftLog
- id
- user_id
- exercise
- weight
- reps
- date

### LeaderboardEntry
- id
- user_id
- bodyweight
- exercise
- weight
- reps
- age
- score

---

## 7. System Logic

### Training Weight Calculation
weight = 1RM × percentage

### Rounding Rule
Round to nearest 2.5kg

---

## 8. User Flow

1. User registers and inputs 1RM values
2. User logs in
3. User selects a lift from homepage
4. System displays program with calculated weights
5. User completes workout and logs lifts
6. System provides feedback
7. User can submit results to leaderboard

---

## 9. Future Enhancements

- Graphs for progress tracking
- Advanced program selection
- Social features (friends, sharing)
- Mobile application
