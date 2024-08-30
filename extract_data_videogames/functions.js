const readline = require('readline');
const fs = require('fs');

const apiKey = 'x';
const apiUrl = 'https://api.rawg.io/api/games';
const jsonFilePathPrefix = '../files/json/games';
const csvFilePathPrefix = '../files/csv/games';
let batchCounter = 1;
let games = [];
const pageSize = 40;
const pagesPerBatch = 1;
let pagesCounter = 0;
totalPage = 1;
totalTiradas = pagesPerBatch;


function initProccess() {
  console.log('Bienvenido!');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question('¿Deseas iniciar el proceso? Si(s) No(n)) ', (answer) => {
    if (answer.toLowerCase() === 's') {
      console.log('Iniciando el proceso...');
      fetchAndSaveGames()
    } else if (answer.toLowerCase() === 'n') {
      console.log('Proceso cancelado.');
    } else {
      console.log('Respuesta no válida. Por favor, responde "Si(s)" o "No(n)".');
    }
    rl.close();
  });
}

//Extraer una página de juegos de la API
async function fetchGames(page = 21755) {
  try {
    // const url = `${apiUrl}?key=${apiKey}&page=${page}&page_size=${pageSize}`;
    //const url = `${apiUrl}?key=${apiKey}&page=${page}&page_size=${pageSize}&platforms=4,5,187,18,16,15,27,19,1,186,14,80,7,8,9,13,10,11,105,83,24,43,26,79,49`;
    //const url = `${apiUrl}?key=${apiKey}&page=${page}&page_size=${pageSize}&platforms=1,4,5,7,8,9,10,11,13,14,15,16,18,19,24,26,27,43,49,79,80,83,105,186,187`;
    const url = `${apiUrl}?key=${apiKey}&page=${page}&page_size=${pageSize}`;
    //const url = `${apiUrl}?key=${apiKey}&page=${page}&page_size=${pageSize}&platforms=1,4,5,7,8,9,10,11,13,14,15,16,18,19,24,26,27,43,49,79,80,83,105,186,187`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error en la solicitud: ${response.status}`);
    }
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error(`Hubo un problema con la solicitud: ${error.message}`);
    return null;
  }
}

//LLamada a fetchGames y crear json y csv
async function fetchAndSaveGames(page = 1) {
  const gamesResponse = await fetchGames(page);

  if (gamesResponse === null) {
    // Continuar con la siguiente solicitud
    setTimeout(() => {
      fetchAndSaveGames(page + 1);
    }, 1500); // Esperar 1.5 segundos antes de la siguiente solicitud
    return;
  }

  if (gamesResponse.length > 0) {
    // Guardar los juegos
    games = games.concat(gamesResponse);

    //gamesResponse.forEach(game => {
      //console.log(game.name); // Imprime el nombre del juego
    //});
    
    // for (var i = 0; i < gamesResponse.length; i++) {
    //   console.log('game: '+gamesResponse.stringify())
    // }

    // Incrementar el contador de páginas
    console.log('Página solicitada: ' +pagesCounter+' de la tirada '+batchCounter)
    console.log('Total páginas (intentos) solicitadas: ' + (page))
    pagesCounter++;
    totalPage++

    // Verificar si se alcanzó el límite de páginas por lote
    if (pagesCounter === pagesPerBatch) {
      console.log('Se va a proceder a guardar las ultimas ' + pagesCounter + ' páginas de un total de '+totalTiradas)
      // Guardar los juegos en el archivo JSON
      const jsonFilePath = `${jsonFilePathPrefix}${batchCounter}.json`;
      fs.writeFileSync(jsonFilePath, JSON.stringify(games, null, 2));
      console.log(`Archivo JSON '${jsonFilePath}' creado correctamente.`);

      // Guardar los juegos en el archivo CSV
      const csvFilePath = `${csvFilePathPrefix}${batchCounter}.csv`;
      const headers = ['id', 'slug', 'released', 'tba', 'background_image', 'rating', 'rating_top', 'game_ratings_title', 'game_ratings_count', 'game_ratings_percent', 'reviews_text_count', 'added', 'added_by_status_title', 'added_by_status_values', 'metacritic', 'playtime', 'suggestions_count', 'reviews_count', 'esrb_rating_id', 'esrb_rating_name', 'esrb_rating_slug', 'platforms', 'platforms_games_count', 'platforms_image_background', 'released_at', 'parent_platforms', 'genres', 'stores', 'stores_games_count', 'stores_image_background', 'tags', 'tags_language', 'tags_games_count'];

      const csvContent = games.map(game => {
        //game.id
        game_id = ""
        if (game.id != null) { game_id = game.id }
        //game_slug
        game_slug = ""
        if (game.slug != null) { game_slug = game.slug }
        //game_name
        // game_name = ""
        // if (game.name != null) { game_name = game.name }
        //game_released
        game_released = ""
        if (game.released != null) { game_released = game.released }
        //game_tba
        game_tba = false
        if (game.tba != null) { game_tba = game.tba }
        //game_background_image
        game_background_image = ""
        if (game.background_image != null) { game_background_image = game.background_image }
        //game_rating
        game_rating = ""
        if (game.rating != null) { game_rating = game.rating }
        //game_rating_top
        game_rating_top = ""
        if (game.rating_top != null) { game_rating_top = game.rating_top }
        //game_ratings_count
        // game_ratings_count = ""
        // if (game.ratings_count != null) { game_ratings_count = game.ratings_count }
        //game_reviews_text_count
        game_reviews_text_count = ""
        if (game.reviews_text_count != null) { game_reviews_text_count = game.reviews_text_count }
        //game_added
        game_added = ""
        if (game.added != null) { game_added = game.added }
        // //game_added
        // game_added = ""
        // if (game.added != null) { game_added = game.added }
        //game_metacritic
        game_metacritic = ""
        if (game.metacritic != null) { game_metacritic = game.metacritic }
        //game_metacritic
        game_playtime = ""
        if (game.playtime != null) { game_playtime = game.playtime }
        //game_metacritic
        game_suggestions_count = ""
        if (game.suggestions_count != null) { game_suggestions_count = game.suggestions_count }
        //game_reviews_count
        game_reviews_count = ""
        if (game.reviews_count != null) { game_reviews_count = game.reviews_count }
        //Guardar las platforms
        let platforms = ""
        platforms = game.platforms.map(platformObj => platformObj && platformObj.platform.slug).join(',');
        //Guardar las platforms_games_count
        let platforms_games_count = ""
        platforms_games_count = game.platforms.map(platformObj => platformObj && platformObj.platform.games_count).join(',');
        //Guardar las platforms_image_background
        let platforms_image_background = ""
        platforms_image_background = game.platforms.map(platformObj => platformObj && platformObj.platform.image_background).join(',');
        //Guardar las released_at (fechas  de salida)
        let released_at = ""
        released_at = game.platforms.map(platformObj => platformObj && platformObj.released_at).join(',');
        //Guardar las parent_platforms
        let parent_platforms = ""
        parent_platforms = game.parent_platforms.map(platformObj => platformObj && platformObj.platform.slug).join(',');
        //Guardar las genres
        let genres = ""
        genres = game.genres.map(platformObj => platformObj && platformObj.slug).join(',');
        //Guardar las stores_slug
        let stores = ""
        stores = game.stores.map(platformObj => platformObj && platformObj.store.slug).join(',');
        //Guardar las stores_games_count
        let stores_games_count = ""
        stores_games_count = game.stores.map(platformObj => platformObj && platformObj.store.games_count).join(',');
        //Guardar las stores_image_background
        let stores_image_background = ""
        stores_image_background = game.stores.map(platformObj => platformObj && platformObj.store.image_background).join(',');
        //Guardar las tags
        let tags = ""
        tags = game.tags.map(platformObj => platformObj && platformObj.slug).join(',');
        //Guardar las tags_language
        let tags_language = ""
        tags_language = game.tags.map(platformObj => platformObj && platformObj.language).join(',');
        //Guardar las tags_games_count 
        let tags_games_count = ""
        tags_games_count = game.tags.map(platformObj => platformObj && platformObj.games_count).join(',');
        //esrb_rating
        let esrb_rating = { id: "", name: "", slug: "" }
        if (game.esrb_rating != null) {
          esrb_rating.id = game.esrb_rating.id
          esrb_rating.name = game.esrb_rating.name
          esrb_rating.slug = game.esrb_rating.slug
        }
        //ratings
        let game_ratings = { exceptional_count: "", exceptional_percent: "", recommended_count: "", recommended_percent: "", meh_count: "", meh_percent: "", skip_count: "", skip_percent: "" }
        // if (game.ratings != null && game.ratings.length < 0) {
        let game_ratings_title = ""
        let game_ratings_count = ""
        let game_ratings_percent = ""
        if (game.ratings != null) {
          game_ratings_title = game.ratings.map(platformObj => platformObj && platformObj.title).join(',');
          game_ratings_count = game.ratings.map(platformObj => platformObj && platformObj.count).join(',');
          game_ratings_percent = game.ratings.map(platformObj => platformObj && platformObj.percent).join(',');
          //   if (game.ratings[0] && game.ratings[0] !== undefined && game.ratings[0].count && game.ratings[0].count != null) {
          //     game_ratings.exceptional_count = game.ratings[0].count
          //   }
          //   if (game.ratings[0].percent && game.ratings[0].percent != null) {
          //     game_ratings.exceptional_percent = game.ratings[0].percent
          //   }
          //   if (game.ratings[1] && game.ratings[1] !== undefined && game.ratings[1].count && game.ratings[1].count != null) {
          //     game_ratings.recommended_count = game.ratings[1].count
          //   }
          //   if (game.ratings[1] && game.ratings[1] !== undefined && game.ratings[1].percent && game.ratings[1].percent != null) {
          //     game_ratings.recommended_percent = game.ratings[1].percent
          //   }
          //   if (game.ratings[2] && game.ratings[2] !== undefined && game.ratings[2].count && game.ratings[2].count != null) {
          //     game_ratings.meh_count = game.ratings[2].count
          //   }
          //   if (game.ratings[2] && game.ratings[2] !== undefined && game.ratings[2].percent && game.ratings[2].percent != null) {
          //     game_ratings.meh_percent = game.ratings[2].percent
          //   }
          //   if (game.ratings[3] && game.ratings[3] !== undefined && game.ratings[3].count && game.ratings[3].count != null && game.ratings[3].count !== undefined) {
          //     game_ratings.skip_count = game.ratings[3].count
          //   }
          //   if (game.ratings[3] && game.ratings[3] !== undefined && game.ratings[3].percent && game.ratings[3].percent != null && game.ratings[3].percent !== undefined) {
          //     game_ratings.skip_percent = game.ratings[3].percent
          //   }
        }
        //added_by_status
        let added_by_status_title = ""
        let added_by_status_values = ""
        // let added_by_status = { yet: "", owned: "", beaten: "", toplay: "", dropped: "", playing: "" }
        if (game.added_by_status != null) {
          added_by_status_title = Object.keys(game.added_by_status).join(',');
          added_by_status_values = Object.values(game.added_by_status).join(',');
          // added_by_status.yet = game.added_by_status.yet
          // added_by_status.owned = game.added_by_status.owned
          // added_by_status.beaten = game.added_by_status.beaten
          // added_by_status.toplay = game.added_by_status.toplay
          // added_by_status.dropped = game.added_by_status.dropped
          // added_by_status.playing = game.added_by_status.playing
        }

        //return para escribir csv
        return `${game_id}|${game_slug}|${game_released}|${game_tba}| ${game_background_image} |${game_rating}|${game_rating_top}|${game_ratings_title}|${game_ratings_count}|${game_ratings_percent}|${game_reviews_text_count}|${game_added}|${added_by_status_title}|${added_by_status_values}|${game_metacritic}|${game_playtime}|${game_suggestions_count}|${game_reviews_count}|${esrb_rating.id}|${esrb_rating.name}|${esrb_rating.slug}|${platforms}|${platforms_games_count}|${platforms_image_background}|${released_at}|${parent_platforms}|${genres}|${stores}|${stores_games_count}|${stores_image_background}|${tags}|${tags_language}|${tags_games_count}`;
      }).join('\n');

      fs.writeFileSync(csvFilePath, '\uFEFF' + headers.join(',') + '\n' + csvContent, { encoding: 'utf8' });
      console.log(`Archivo CSV '${csvFilePath}' creado correctamente.`);

      // Reiniciar el array de juegos, el contador de páginas y aumentar el contador de lotes
      games = [];
      pagesCounter = 0;
      batchCounter++;
      totalTiradas = totalTiradas + 500;
    }

    // Continuar con la siguiente solicitud
    setTimeout(() => {
      fetchAndSaveGames(page + 1);
    }, 1500); // Esperar 1 segundo antes de la siguiente solicitud
  } else {
    console.log('No hay más juegos que guardar. Proceso completado.');
  }
}

module.exports = { initProccess };
