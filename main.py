from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

@dataclass
class State:
    activity_type: str
    experience_level: str
    available_minutes: int
    practice_schedule: list 
    completed_activities: list 
    practice_sessions: list 
    practice_goal: str 
    goal_activity: str 
    goal_frequency: int 
    goal_duration: int
    
@dataclass
class PracticeActivity:
    activity_name: str
    activity_type: str
    difficulty: str
    duration: int
    completed: bool
    
@route
def back_home(state: State) -> Page:
    """
    Takes in the current state and return the home page
    """
    return home_page(state)

def style_button(button):
    """
    Changes the background color and text color of buttons
    """
    button = change_background_color(button, "#a855f7")
    button = change_color(button, "white")
    return button

def style_title(box):
    """
    Changes the background color, text color, size, and text alginment of titles.
    """
    box = change_background_color(box, "#fdf2f8")
    box = change_color(box, "#6b21a8")
    box = change_padding(box, "20px")
    box = change_text_align(box, "center")
    return box


def style_card(box):
    """
    Changes the background color, text color, and size of cards.
    """
    box = change_background_color(box, "white")
    box = change_color(box, "#6b21a8")
    box = change_padding(box, "10px")
    return box


def home_page(state: State) -> Page:
    """
    Takes in the current state and returns the home page showing the welcome box and the three buttons.
    """
    welcome_box = Div(
        Header("Welcome to the Practice Planner!"),
        "Build practice schedules for singing and dancing, and track your goals.",
    )
    welcome_box = change_background_color(welcome_box, "#fdf2f8")
    welcome_box = change_color(welcome_box, "#6b21a8")
    welcome_box = change_padding(welcome_box, "20px")
    welcome_box = change_text_align(welcome_box, "center")

    return Page(state, [
        welcome_box,
        style_button(Button("Create a practice schedule", create_schedule)),
        style_button(Button("Set my goals", set_new_goal)),
        style_button(Button("View my progress", view_progress)),
    ])

@route
def index(state: State) -> Page:
    """
    Takes in the current state and returns the home page.
    """
    return home_page(state)

@route
def create_schedule(state: State) -> Page:
    """
    Takes in the current state and returns the page to create your schedule.
    """
    return create_schedule_page(state)

def create_schedule_page(state: State) -> Page:
    """
    Takes in the current state and returns the page to create your schedule which has the title, asks which activity
    you would like to practice, your experience level, and how much time you have. It also has two buttons.
    """
    return Page(state, [
        style_title(Div(Header("Create a Practice Schedule"))),

        style_card(Div("What would you like to practice?",
                       SelectBox("activity_type", ["Singing", "Dancing", "Both"], state.activity_type))),
        "\n",
        style_card(Div("What is your experience level?",
                       SelectBox("experience_level", ["Beginner", "Intermediate", "Advanced"], state.experience_level))),
        "\n",
        style_card(Div("How much time do you have (in minutes)?",
                       SelectBox("available_minutes", ["15", "30", "45", "60"], str(state.available_minutes)))),

        style_button(Button("Back home", back_home)),
        style_button(Button("Generate my schedule", generate_schedule)),
    ])

@route
def generate_schedule(state: State, activity_type: str, experience_level: str, available_minutes: int) -> Page:
    """
    Takes in the current state, the activity type the user selected, the experience level the user selected,
    and how many available minutes the student selected. It returns the schedule page which shows the user their
    generated schedule.
    """
    state.activity_type = activity_type
    state.experience_level = experience_level
    state.available_minutes = available_minutes
    state.completed_activities = []

    if activity_type == "Both":
        half = available_minutes // 2
        state.practice_schedule = (
            build_activities("Singing", experience_level, half)
            + build_activities("Dancing", experience_level, available_minutes - half)
        )
    else:
        state.practice_schedule = build_activities(activity_type, experience_level, available_minutes)

    return schedule_page(state)

def build_activities(kind: str, level: str, minutes: int) -> list[PracticeActivity]:
    """
    It takes in the kind of activity the user chose, the level they chose, and the amount of minutes they chose.
    It returns a list of the generated practice activities for the warm up, main activity, and cool down based
    on what options they chose.
    """
    warmup_time = minutes // 5
    cooldown_time = minutes // 5
    main_time = minutes - warmup_time - cooldown_time

    if kind == "Singing":
        warmup_name = "Vocal Warm-ups"
        cooldown_name = "Vocal Cool-down"
        if level == "Beginner":
            main_name = "Scales and Breath Control"
        elif level == "Intermediate":
            main_name = "Song Practice"
        else:
            main_name = "Performance Run-Through"
    else:
        warmup_name = "Dance Warm-up"
        cooldown_name = "Stretching"
        if level == "Beginner":
            main_name = "Basic Steps"
        elif level == "Intermediate":
            main_name = "Choreography"
        else:
            main_name = "Freestyle and Performance Practice"

    return [
        PracticeActivity(warmup_name, kind, level, warmup_time, False),
        PracticeActivity(main_name, kind, level, main_time, False),
        PracticeActivity(cooldown_name, kind, level, cooldown_time, False),
    ]


def schedule_page(state: State) -> Page:
    """
    Takes in the current state and returns the schedule page which has each activity in the user's generated schedule
    listed with how long to spend on that activity. It also has check boxes to check off the activities when they are
    completed. It has two buttons.
    """
    content = [style_title(Div(Header("Your Practice Schedule")))]

    for i in range(len(state.practice_schedule)):
        activity = state.practice_schedule[i]
        label = activity.activity_name + " (" + str(activity.duration) + " minutes)"
        content.append(style_card(Div(label, CheckBox("activity_" + str(i), activity.completed))))

    content.append(style_button(Button("Save completed session", save_completed_session)))
    content.append(style_button(Button("View my progress", view_progress)))

    return Page(state, content)

@route
def save_completed_session(state: State, activity_0: bool = False, activity_1: bool = False,
                           activity_2: bool = False, activity_3: bool = False,
                           activity_4: bool = False, activity_5: bool = False) -> Page:
    """
    It takes in the current state and all of the checkboxes for the activities set to false as their default if there
    is no value for that activity. It returns the progress page that is updated with the session that was
    just completed.
    """
    checked = [activity_0, activity_1, activity_2, activity_3, activity_4, activity_5]

    state.completed_activities = []
    minutes = 0

    for i in range(len(state.practice_schedule)):
        activity = state.practice_schedule[i]
        activity.completed = checked[i]
        if checked[i]:
            state.completed_activities.append(activity)
            minutes = minutes + activity.duration

    if minutes > 0:
        record = PracticeActivity("Practice Session", state.activity_type,
                                  state.experience_level, minutes, True)
        state.practice_sessions.append(record)

    return progress_page(state)

@route
def view_progress(state: State) -> Page:
    """
    Takes in the current state and returns the progress page.
    """
    return progress_page(state)


def count_sessions(state: State, activity_type: str) -> int:
    """
    Takes in the current state and the activity type and counts how many times that activity was practiced.
    It returns that number as an integer.
    """
    count = 0
    for session in state.practice_sessions:
        if session.activity_type == activity_type or session.activity_type == "Both":
            count = count + 1
    return count


def progress_page(state: State) -> Page:
    """
    Takes in the current state and returns the progress page which displays the total number of sessions.
    the total minutes practiced, the number of singing sessions, the number of dancing sessions, any set goals and
    their status, and two buttons.
    """
    total_sessions = len(state.practice_sessions)

    total_minutes = 0
    for session in state.practice_sessions:
        total_minutes = total_minutes + session.duration

    singing_sessions = count_sessions(state, "Singing")
    dancing_sessions = count_sessions(state, "Dancing")

    # Goal status
    if state.practice_goal == "":
        goal_text = "You haven't set a goal yet."
        goal_status = ""
    else:
        goal_text = state.practice_goal + " (" + state.goal_activity + ")"
        target = state.goal_frequency * state.goal_duration
        done = count_sessions(state, state.goal_activity)
        if done >= target:
            goal_status = "Status: Completed!"
        else:
            goal_status = "Status: In progress (" + str(done) + " of " + str(target) + " sessions)"

    return Page(state, [
        style_title(Div(Header("Your Progress"))),

        style_card(Div(Header("Practice Goal", 2), goal_text, LineBreak(), goal_status)),
        style_card(Div(Header("Practice Statistics", 2),
                       "Sessions completed: " + str(total_sessions), LineBreak(),
                       "Minutes practiced: " + str(total_minutes))),
        style_card(Div(Header("Practice History", 2),
                       "Singing sessions: " + str(singing_sessions), LineBreak(),
                       "Dancing sessions: " + str(dancing_sessions))),

        style_button(Button("Create new schedule", create_schedule)),
        style_button(Button("Back home", back_home)),
    ])

@route
def set_new_goal(state: State) -> Page:
    """
    Takes in the current state and returns the goal setting page.
    """
    return goal_setting_page(state)


def goal_setting_page(state: State) -> Page:
    """
    Takes in the current state and returns the goal setting page which has the title, and the questions to set
    your goal which are what your goal is, what hobby it is for, how often the user wants to practice, and how long
    the user wants to work toward this goal.
    """
    return Page(state, [
        style_title(Div(Header("Set My Goals"))),

        style_card(Div("What is your goal?",
                       TextBox("practice_goal", state.practice_goal))),
        "\n",
        style_card(Div("Which hobby is this goal for?",
                       SelectBox("goal_activity", ["Singing", "Dancing"], state.goal_activity))),
        "\n",
        style_card(Div("How many days per week do you want to practice?",
                       SelectBox("goal_frequency", ["1", "2", "3", "4", "5"], str(state.goal_frequency)))),
        "\n",
        style_card(Div("How many weeks do you want to work toward this goal?",
                       SelectBox("goal_duration", ["1", "2", "3", "4"], str(state.goal_duration)))),

        "\n",
        style_button(Button("Save my goal", save_goal)),
        style_button(Button("Back home", back_home)),
    ])

@route
def save_goal(state: State, practice_goal: str, goal_activity: str,
              goal_frequency: int, goal_duration: int) -> Page:
    """
    Takes in the current state, the practice goal, the goal activity, the goal frequency, and the goal duration and
    returns the progress page that is updated with the newly set goal.
    """
    state.practice_goal = practice_goal
    state.goal_activity = goal_activity
    state.goal_frequency = goal_frequency
    state.goal_duration = goal_duration

    return progress_page(state)

assert_equal(
    build_activities("Singing", "Beginner", 15),
    [
        PracticeActivity("Vocal Warm-ups", "Singing", "Beginner", 3, False),
        PracticeActivity("Scales and Breath Control", "Singing", "Beginner", 9, False),
        PracticeActivity("Vocal Cool-down", "Singing", "Beginner", 3, False),
    ])

assert_equal(
    build_activities("Dancing", "Intermediate", 30),
    [
        PracticeActivity("Dance Warm-up", "Dancing", "Intermediate", 6, False),
        PracticeActivity("Choreography", "Dancing", "Intermediate", 18, False),
        PracticeActivity("Stretching", "Dancing", "Intermediate", 6, False),
    ])

assert_equal(
    build_activities("Singing", "Advanced", 60),
    [
        PracticeActivity("Vocal Warm-ups", "Singing", "Advanced", 12, False),
        PracticeActivity("Performance Run-Through", "Singing", "Advanced", 36, False),
        PracticeActivity("Vocal Cool-down", "Singing", "Advanced", 12, False),
    ])

assert_equal(
    build_activities("Dancing", "Beginner", 45),
    [
        PracticeActivity("Dance Warm-up", "Dancing", "Beginner", 9, False),
        PracticeActivity("Basic Steps", "Dancing", "Beginner", 27, False),
        PracticeActivity("Stretching", "Dancing", "Beginner", 9, False),
    ])

singing_session = PracticeActivity("Practice Session", "Singing", "Beginner", 15, True)
dancing_session = PracticeActivity("Practice Session", "Dancing", "Beginner", 30, True)
both_session = PracticeActivity("Practice Session", "Both", "Beginner", 45, True)

no_sessions = State("Singing", "Beginner", 15, [], [], [], "", "Singing", 1, 1)
mixed_sessions = State("Singing", "Beginner", 15, [], [],
                       [singing_session, dancing_session], "", "Singing", 1, 1)
with_both = State("Singing", "Beginner", 15, [], [],
                  [singing_session, both_session], "", "Singing", 1, 1)
mostly_dancing = State("Singing", "Beginner", 15, [], [],
                       [dancing_session, dancing_session, both_session], "", "Singing", 1, 1)

assert_equal(count_sessions(no_sessions, "Singing"), 0)
assert_equal(count_sessions(mixed_sessions, "Singing"), 1)
assert_equal(count_sessions(mixed_sessions, "Dancing"), 1)
assert_equal(count_sessions(with_both, "Singing"), 2)
assert_equal(count_sessions(with_both, "Dancing"), 1)
assert_equal(count_sessions(mostly_dancing, "Dancing"), 3)
assert_equal(count_sessions(mostly_dancing, "Singing"), 1)

add_website_css("body", "background-color: #fdf2f8;")
set_site_information(
    author = "Shaina Berkowitz",
    description = "A webiste that builds practice schedules for singers and dancers, and tracks goals and progress.",
    sources = [
        "Drafter documentation"
        "Claude AI"
    ],
    planning = [""]
    links = [""]
)
set_website_title("Practice Planner")
set_website_framed(False)
hide_debug_information()
start_server(State("Singing", "Beginner", 15, [], [], [], "", "Singing", 1, 1))
