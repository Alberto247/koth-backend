const SERVER_URL = "https://backend.registry.alberto247.xyz:7394"
async function apiLogin(username, password){ //Try login
    try{
        const data = {username:username, password:password};
        const res = await fetch(SERVER_URL+'/login', {
            credentials: 'include',
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        if(!res.ok){
            return false;
        }
        return true;
    } catch(exception){
        console.error(exception);
    }
}

async function apiIsLoggedIn(){ //Retrieve user's data if logged in
    try{
        const res = await fetch(SERVER_URL+'/me', {
            credentials: 'include'
        })
        if(!res.ok){
            return false;
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiLogout(){ //logout
    try{
        const res = await fetch(SERVER_URL+'/logout', {
            credentials: 'include'
        })
        if(!res.ok){
            return false;
        }
        return true;
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGames(){ //get all exams
    try{
        const res = await fetch(SERVER_URL+'/games')
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGameRounds(game){ //get number of enrolled students in course
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/rounds')
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGameFinalScoreboard(game){ //get user study plan
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/scoreboard', {
            credentials: 'include'
        })
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGameRoundScoreboard(game, round){ //get exam by code
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/'+round+'/scoreboard')
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGameRoundHistory(game, round){ //get exam by code
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/'+round+'/history')
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGamesScoreboard(games){
    try{
        const data = {games:games};
        const res = await fetch(SERVER_URL+'/games/scoreboards', {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        if(!res.ok){
            return {};
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

export {
    apiLogin,
    apiIsLoggedIn,
    apiLogout,
    apiGetGames,
    apiGetGameRounds,
    apiGetGameFinalScoreboard,
    apiGetGameRoundScoreboard,
    apiGetGameRoundHistory,
    apiGetGamesScoreboard
}