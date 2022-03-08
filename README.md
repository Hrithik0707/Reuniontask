# Reuniontask

## Task Completed with all the given API Endpoints.
## Test these endpoints on Postman.

# API'S Hosted on :     https://runiontask.herokuapp.com/


# Rules to run API Endpoints:
1. (POST) https://runiontask.herokuapp.com/api/register
     INPUT: email,first_name, password
     
2. (POST) https://runiontask.herokuapp.com/api/authenticate 
    - INPUT: Email, Password
    - RETURN: JWT token

Add JWT token to Header in Authorization in format 'Bearer {token}'

4.(POST) https://runiontask.herokuapp.com/api/follow/{id}  
      - INPUT: id

5.(POST) https://runiontask.herokuapp.com/api/unfollow/{id}  
      - INPUT: id
      
6.(GET) https://runiontask.herokuapp.com/api/user

7.(POST) https://runiontask.herokuapp.com/api/posts/ 
    - INPUT: title,description
  
8.(DELETE) https://runiontask.herokuapp.com/api/posts/{id}

9.(POST) https://runiontask.herokuapp.com/api/like/{id} 

10. (POST) https://runiontask.herokuapp.com/api/unlike/{id} 

11. (POST) https://runiontask.herokuapp.com/api/comment/{id}
           - INPUT: comment

12. (GET) https://runiontask.herokuapp.com/api/posts/{id}

13.(GET) https://runiontask.herokuapp.com/api/all_posts
