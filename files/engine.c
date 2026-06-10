#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define MAX_EVENTS 100
#define MAX_TITLE 100
#define MAX_CATEGORY 30
#define MAX_LOCATION 100

typedef struct {
    int id;                   
    char title[MAX_TITLE];    
    char category[MAX_CATEGORY]; 
    char location[MAX_LOCATION]; 
    int deadline;
    int urgency;              
    int importance;            
    int guests;
    float budget;            
    int priority_score;        
    int status;              
    int created_day;
} Event;

// Global event storage
Event events[MAX_EVENTS];
int event_count = 0;

int calculate_priority_score(int deadline, int urgency, int importance) {
  
    int deadline_weight = 100 - (deadline * 10); 
    if (deadline <= 3) {
        deadline_weight *= 2; s
    }
    
  
    int urgency_weight = urgency * 15;    
    int importance_weight = importance * 12;

    int final_score = deadline_weight + urgency_weight + importance_weight;
    

    return (final_score > 0) ? final_score : 10;
}


int add_event(char title[], char category[], char location[], 
              int deadline, int urgency, int importance, 
              int guests, float budget) {
    
 
    if (event_count >= MAX_EVENTS) {
        return 0;
    }
    
    if (deadline < 1 || deadline > 365) {
        return 0;  // Invalid deadline
    }
    
    if (urgency < 1 || urgency > 10 || importance < 1 || importance > 10) {
        return 0;  // Invalid urgency or importance
    }
    

    events[event_count].id = event_count + 1;
    strncpy(events[event_count].title, title, MAX_TITLE - 1);
    events[event_count].title[MAX_TITLE - 1] = '\0';
    
    strncpy(events[event_count].category, category, MAX_CATEGORY - 1);
    events[event_count].category[MAX_CATEGORY - 1] = '\0';
    
    strncpy(events[event_count].location, location, MAX_LOCATION - 1);
    events[event_count].location[MAX_LOCATION - 1] = '\0';
    
    events[event_count].deadline = deadline;
    events[event_count].urgency = urgency;
    events[event_count].importance = importance;
    events[event_count].guests = guests;
    events[event_count].budget = budget;
    events[event_count].status = 0;  // Pending
    events[event_count].created_day = (int)time(NULL);
    
    // Calculate smart priority score
    events[event_count].priority_score = calculate_priority_score(
        deadline, urgency, importance
    );
    
    event_count++;
    return 1;  // Success
}


int delete_event(int event_id) {
    // Find event by ID
    int index = -1;
    for (int i = 0; i < event_count; i++) {
        if (events[i].id == event_id) {
            index = i;
            break;
        }
    }
    
    // If not found, return failure
    if (index == -1) {
        return 0;
    }
    
    // Shift all events after this one
    for (int i = index; i < event_count - 1; i++) {
        events[i] = events[i + 1];
    }
    
    event_count--;
    return 1;  // Success
}


void sort_by_priority() {
    // Bubble sort: compare adjacent events and swap if needed
    for (int i = 0; i < event_count; i++) {
        for (int j = 0; j < event_count - i - 1; j++) {
            // If current event has lower priority than next, swap them
            if (events[j].priority_score < events[j + 1].priority_score) {
                Event temp = events[j];
                events[j] = events[j + 1];
                events[j + 1] = temp;
            }
        }
    }
}

void sort_by_deadline() {
    for (int i = 0; i < event_count; i++) {
        for (int j = 0; j < event_count - i - 1; j++) {
            if (events[j].deadline > events[j + 1].deadline) {
                Event temp = events[j];
                events[j] = events[j + 1];
                events[j + 1] = temp;
            }
        }
    }
}


void get_all_events(char *result, int max_len) {
    char buffer[8000] = "{\"events\":[";
    
    for (int i = 0; i < event_count; i++) {
        char event_json[500];
        sprintf(event_json, 
            "{\"id\":%d,\"title\":\"%s\",\"category\":\"%s\",\"location\":\"%s\","
            "\"deadline\":%d,\"urgency\":%d,\"importance\":%d,\"guests\":%d,"
            "\"budget\":%.2f,\"priority_score\":%d,\"status\":%d}",
            events[i].id,
            events[i].title,
            events[i].category,
            events[i].location,
            events[i].deadline,
            events[i].urgency,
            events[i].importance,
            events[i].guests,
            events[i].budget,
            events[i].priority_score,
            events[i].status
        );
        
        strcat(buffer, event_json);
        
       
        if (i < event_count - 1) {
            strcat(buffer, ",");
        }
    }
    
    strcat(buffer, "]}");
    strncpy(result, buffer, max_len - 1);
    result[max_len - 1] = '\0';
}

void generate_schedule(char *result, int max_len) {
    Event temp_events[MAX_EVENTS];
    for (int i = 0; i < event_count; i++) {
        temp_events[i] = events[i];
    }
    
    // Sort by priority score (highest first) for smart scheduling
    for (int i = 0; i < event_count; i++) {
        for (int j = 0; j < event_count - i - 1; j++) {
            if (temp_events[j].priority_score < temp_events[j + 1].priority_score) {
                Event temp = temp_events[j];
                temp_events[j] = temp_events[j + 1];
                temp_events[j + 1] = temp;
            }
        }
    }

    char buffer[8000] = "{\"schedule\":[";
    
    for (int i = 0; i < event_count; i++) {
        char event_json[500];
        sprintf(event_json, 
            "{\"id\":%d,\"title\":\"%s\",\"category\":\"%s\",\"location\":\"%s\","
            "\"deadline\":%d,\"urgency\":%d,\"importance\":%d,\"budget\":%.2f,"
            "\"priority_score\":%d,\"position\":%d}",
            temp_events[i].id,
            temp_events[i].title,
            temp_events[i].category,
            temp_events[i].location,
            temp_events[i].deadline,
            temp_events[i].urgency,
            temp_events[i].importance,
            temp_events[i].budget,
            temp_events[i].priority_score,
            i + 1  // Position in schedule
        );
        
        strcat(buffer, event_json);
        
        if (i < event_count - 1) {
            strcat(buffer, ",");
        }
    }
    
    strcat(buffer, "]}");
    strncpy(result, buffer, max_len - 1);
    result[max_len - 1] = '\0';
}


void get_analytics(char *result, int max_len) {
    float total_budget = 0;
    int total_guests = 0;
    int completed = 0;
    int pending = 0;
    float avg_importance = 0;
    
    for (int i = 0; i < event_count; i++) {
        total_budget += events[i].budget;
        total_guests += events[i].guests;
        if (events[i].status == 2) completed++;
        if (events[i].status == 0) pending++;
        avg_importance += events[i].importance;
    }
    
    if (event_count > 0) {
        avg_importance /= event_count;
    }
    
    sprintf(result, 
        "{\"total_events\":%d,\"total_budget\":%.2f,\"total_guests\":%d,"
        "\"completed\":%d,\"pending\":%d,\"avg_importance\":%.1f}",
        event_count, total_budget, total_guests, completed, pending, avg_importance
    );
}


int update_event_status(int event_id, int new_status) {
    // Find event
    for (int i = 0; i < event_count; i++) {
        if (events[i].id == event_id) {
            // Validate status (0: Pending, 1: In Progress, 2: Completed)
            if (new_status >= 0 && new_status <= 2) {
                events[i].status = new_status;
                return 1;  // Success
            }
            return 0;  // Invalid status
        }
    }
    return 0;  // Event not found
}


void search_events(char *query, char *result, int max_len) {
    char buffer[8000] = "{\"results\":[";
    int found = 0;
    
    for (int i = 0; i < event_count; i++) {
        // Check if query matches title or category (case-insensitive)
        if (strstr(events[i].title, query) != NULL || 
            strstr(events[i].category, query) != NULL) {
            
            if (found > 0) strcat(buffer, ",");
            
            char event_json[500];
            sprintf(event_json, 
                "{\"id\":%d,\"title\":\"%s\",\"category\":\"%s\",\"deadline\":%d,"
                "\"priority_score\":%d}",
                events[i].id,
                events[i].title,
                events[i].category,
                events[i].deadline,
                events[i].priority_score
            );
            
            strcat(buffer, event_json);
            found++;
        }
    }
    
    strcat(buffer, "]}");
    strncpy(result, buffer, max_len - 1);
    result[max_len - 1] = '\0';
}
