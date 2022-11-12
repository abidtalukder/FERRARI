def update_genre_string(genre){
    genre_split = genre_str.split(",");
    if(genre == "adventure"){
        genre_split[0] = int(genre_split[0]) + 1
    }
    elif(genre == "funny"){
        genre_split[1] = int(genre_split[1]) + 1
    }
    elif(genre == "network"){
        genre_split[2] = int(genre_split[2]) + 1
    }
    elif(genre == "scary"){
        genre_split[3] = int(genre_split[3]) + 1
    }
    else{
        genre_split[4] = int(genre_split[4]) + 1
    }
    return genre_split[0] + genre_split[1] + genre_split[2] + genre_split[3] + genre_split[4] 
}

def parse_genre_string(genre_str){
    genre_split = genre_str.split(",");
    # adventure (0), funny (1), network (2), scary (3), science (4)
    curr_max = 0
    for i in range(5):
        genre_split[i] = int(genre_split[i])
        if(genre_split[i] > genre_split[curr_max]){
            curr_max = i
        }
    return i
}