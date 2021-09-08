const happyWrapper = document.querySelector('.happy-wrapper')
const energyWrapper = document.querySelector('.energy-wrapper')
const songWrapper = document.querySelector('.song-wrapper')
const findSong = document.getElementById('findSong')
const errMessage = document.getElementById('errMessage')

function select(e) {
  // make sure the target is the div, not the icon or the wrapper
  let choice
  if (e.target.localName === 'i') {
    choice = e.target.parentElement
  } else if (e.target.classList[0] === 'wrapper') {
    return
  } else {
    choice = e.target
  }
  
  // loop through all options and deselect anything already selected
  for (let option of choice.parentElement.children) {
    if (option.classList.contains('selected')) {
      option.classList.remove('selected')
    }
  }

  // mark the target element as selected
  choice.classList.add('selected')
}

function catcher(e) {
  e.preventDefault();
  songWrapper.innerHTML = ''

  // Check to see if an option was selected for both. User can proceed only if both fields are picked
  const valenceOptions = e.path[1].children[1].children
  const energyOptions = e.path[1].children[3].children
  
  if (!checkValidSelect(valenceOptions, energyOptions)) {
    const errMessage = document.createElement('p')
    errMessage.classList.add('err-message')
    errMessage.innerText = "We cannot pick a song for you until you pick something for both."
    songWrapper.append(errMessage)
    return
  }
  
  // Process the choices to get needed song info
  const choices = document.querySelectorAll('.selected')
  const valence = choices[0].id
  const energy = choices[1].id

  const songInfo = pickSong(valence, energy)

  // Generate the HTML needed to place the song on the catcher
  const {text, iconHTML, uris} = songInfo
  const html = generateHTML(text, iconHTML, uris)
  songWrapper.innerHTML = html
}


/** Helper functions
 * checkValidSelect: checks to see if both options have been selected
 * pickSong
 */
function checkValidSelect(valenceOptions, energyOptions) {
  const valCheck = Array.from(valenceOptions).some(o => o.classList.contains('selected'))
  const enCheck = Array.from(energyOptions).some(o => o.classList.contains('selected'))
  if (valCheck && enCheck) {
    return true
  } else{
    return false
  }
}

function pickSong(valence, energy) {
  if (valence === 'high-val'){
    if (energy === 'high-en'){
      return DEFAULT_SONG_INFO.excited
    } else if (energy === 'med-en') {
      return DEFAULT_SONG_INFO.happy
    } else if (energy === 'low-en') {
      return DEFAULT_SONG_INFO.relaxed
    }
  } else if (valence === 'med-val') {
    if (energy === 'high-en'){
      return DEFAULT_SONG_INFO.curious
    } else if (energy === 'med-en') {
      return DEFAULT_SONG_INFO.bored
    } else if (energy === 'low-en') {
      return DEFAULT_SONG_INFO.tired
    }
  } else if (valence === 'low-val'){
    if (energy === 'high-en'){
      return DEFAULT_SONG_INFO.angry
    } else if (energy === 'med-en') {
      return DEFAULT_SONG_INFO.disappointed
    } else if (energy === 'low-en') {
      return DEFAULT_SONG_INFO.sad
    }
  }
}

function generateHTML(text, iconHTML, uris){
  // Get a random song from the uri list
  const uriIdx = Math.floor(Math.random() * uris.length)
  console.log(uriIdx)
  return `<h4>You most likely feel <span class="wrap" id="${text}">${text}</span></h4>
    <div class="wrapper" id=${text}>
      ${iconHTML}
    </div>
    <iframe src="https://open.spotify.com/embed/track/${uris[uriIdx]}" width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>`
}

happyWrapper.addEventListener('click', select)
energyWrapper.addEventListener('click', select)
findSong.addEventListener('click', catcher)