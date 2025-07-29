import {DataProvider} from "../DataProvider.ts";


export class DownloadController {

    private button: HTMLButtonElement = document.createElement('button');

    constructor() {
        this.button.classList.add("absolute", "z-1000", "bg-white", "border", "border-gray-300", "shadow-lg", "rounded-md", "p-2", 'hover:cursor-pointer', 'hover:bg-gray-100');
        this.button.innerText = "Download";
        this.button.style.top = "0px";
        this.button.style.left = "0px";

        this.button.onclick = this.downloadConfig;

        document.body.appendChild(this.button);
    }


    public downloadConfig() {
        let data = {
            img: {}, map: {}
        };

        for (const [key, value] of DataProvider.getInstance().getAllImgCoords().entries()) { // Using the default iterator (could be `map.entries()` instead)
            data.img[key] = {
                x: value[0],
                y: value[1]
            };
        }
        for (const [key, value] of DataProvider.getInstance().getAllMapCoords().entries()) { // Using the default iterator (could be `map.entries()` instead)
            data.map[key] = {
                latitude: value.lat,
                longitude: value.lng
            };
        }
        let imgBox = document.getElementById('imageBox');

        data['img_scale'] = {
            width: imgBox.clientWidth,
            height: imgBox.clientHeight
        }
        console.log(JSON.stringify(data));
        let blob = new Blob([JSON.stringify(data)], {type: "application/json"});

        let a = document.createElement('a');
        a.download = "data.json";
        a.href = URL.createObjectURL(blob);
        a.dataset.downloadurl = ["application/json", a.download, a.href].join(':');
        a.style.display = "none";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () {
            URL.revokeObjectURL(a.href);
        }, 1500);
    }
}