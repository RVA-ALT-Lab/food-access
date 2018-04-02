const fs = require('fs')
const request = require('request-promise')

let json = fs.readFileSync('food-access-census-richmond.json', {encoding:'utf-8'})

let data = JSON.parse(json)


async function getTractBoundaries(tractData){

        let url = `http://census.ire.org/geo/1.0/boundary-set/tracts/${tractData.CensusTract}`

        try {
            let response = await request(url)
            return response
        } catch (error) {
            return error
        }

}


data.forEach((tract)=>{
    getTractBoundaries(tract)
    .then((data) => console.log(data))
})

fs.writeFileSync('new-data.json', JSON.stringify(data), {encoding: 'utf-8'})