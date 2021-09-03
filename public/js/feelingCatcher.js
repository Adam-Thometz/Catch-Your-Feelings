const happyWrapper = document.querySelector('.happy-wrapper')
const energyWrapper = document.querySelector('.energy-wrapper')
const songWrapper = document.querySelector('.song-wrapper')

function selection(e) {
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

  // mark the target element as selected (deselect )
  choice.classList.add('selected')
}

happyWrapper.addEventListener('click', selection)
energyWrapper.addEventListener('click', selection)