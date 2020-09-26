
function genString() {
	let len = anime.random(10, 69)
	let arr = new Uint8Array(len)
  crypto.getRandomValues(arr)
  return btoa(arr).replace('=', '').substr(0, len)
}

let dmp = new diff_match_patch()
let el = document.querySelector('#scramble-text')

async function scramble(newText) {
	let text = el.textContent
	let diff = dmp.diff_main(text, newText)
	// dmp.diff_cleanupSemantic(diff)
	
	let obj = []
	let rems = []
	let adds = []
	
	el.innerHTML = ''
	for(let str of diff) {
		if(str[0] == -1) {
			let substr = document.createElement('div')
			substr.textContent = str[1]
			substr.className = 'remove'
			rems.push(substr)
			el.appendChild(substr)
		}
		else if(str[0] == 1) {
			let substr = document.createElement('div')
			substr.textContent = str[1]
			substr.className = 'add'
			adds.push(substr)
			el.appendChild(substr)
		}
		else if(str[0] == 0) {
			let substr = document.createElement('div')
			substr.textContent = str[1]
			el.appendChild(substr)
		}
	}
	
	// https://easings.net
	return anime.timeline({duration: 2000, easing: 'easeInOutCubic'})
	.add({targets: rems, width: 0})
	.add({targets: adds, opacity: [0, 1], width: [0, el => el.offsetWidth]}, 0)
	.add({targets: adds, color: '#2196f3', duration: 300})
	.finished.then(() => el.textContent = newText)
}

let strings = [
'Cnwvtus KuaiTaa rl',                                 
'odeeurethn  an Ia_',
'me  p  hagZLngan _',                               
'mrhs baer oag ndC_',                  
'a aeoat dLj lLdio_'
]


var cursor = 0;
// (function start() {
//     scramble(++cursor < strings.length? strings[cursor] : genString()).then(start)
// })()

async function myfunction(){
    let cursor2 = 0;
    while(cursor2 < 5){
        await scramble(strings[cursor2]);
        //await new Promise(r => setTimeout(r, 2000));
        cursor2 = cursor2 + 1;
        console.log(cursor2);
    }
    document.getElementById('scramble-text').innerHTML = "Commander we have setup our base at\n the Khardung La Zoji La Tanglang La and Indira Col";
    document.getElementById('something').innerHTML = "Commanderski";
    //final_test.innerHTML = "Commanderski";
}