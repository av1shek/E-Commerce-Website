function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
 }

 async function send(num) {
    document.querySelector('._2Ujuu').click() 
    document.querySelector('._3guyl').click()
    firstSticker = document.getElementsByClassName('_2YpcJ')[0]

    console.log("sticker Btn", firstSticker)

    let i = 0;
    let j = 0;

    for (i = 0; i < num; i++) {
        for (j = 0; j < 10; j++) {
            firstSticker.click();
        }
        await sleep(1000);
    }
}
send(10)