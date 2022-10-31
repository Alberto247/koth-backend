const SERVER_URL = "https://backend.registry.rising0.com"
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

async function apiGetGames(){ 
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

async function apiGetGameRounds(game){ 
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

async function apiGetGameFinalScoreboard(game){ 
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/scoreboard')
        if(!res.ok){
            return [];
        }
        return await res.json();
    } catch(exception){
        console.error(exception);
    }
}

async function apiGetGameRoundScoreboard(game, round){ 
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

async function apiGetGameRoundHistory(game, round){ 
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

async function apiGetGameRoundOutput(game, round){ 
    try{
        const res = await fetch(SERVER_URL+'/games/'+game+'/'+round+'/output', {
            credentials: 'include'
        })
        if(!res.ok){
            return "";
        }
        return await res.text();
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
    apiGetGamesScoreboard,
    apiGetGameRoundOutput
}