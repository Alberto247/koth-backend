const SIDE = 50

let DRAW // = SVG().addTo('body').size('100%', '100%')
let DRAW_HEX_GROUP // = DRAW.group()
let TEXT_GROUP // = DRAW.group()
// let HIDE_HEXAGON_GROUP // = DRAW.group()

const PLAYER_COLORS = { null: "none", 0: "#008000", 1: "#0000FF", 2: "#FF0000", 3: "#00FFFF", 4: "#FF00FF", 5: "#FFFF00", 6: "salmon", 7: "darkorange", 8: "lime", 9: "violet", 10: "pink", 11: "grey", 12: "royalblue", 13: "palegreen", 14: "peru", 15: "orangered" }
const POINT_TYPES = {
    UNKNOWN_OBJECT: -2,
    UNKNOWN_EMPTY: -1,
    GRASS: 0,
    WALL: 1,
    FORT: 2,
    CRYPTO_CRYSTAL: 3,
    WEB_CRYSTAL: 4,
    REV_CRYSTAL: 5,
    PWN_CRYSTAL: 6,
    MISC_CRYSTAL: 7,
    FLAG: 100,
}

const Hex = Honeycomb.extendHex({
    size: 50,
    // orientation: 'flat',
    point_type: null,
    owner_ID: null,
    current_value: 0
})

const players = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

let hexagon_map = {}
// let hide_hexagon_map = {}
let hex_map = {}
let text_labels = {}
let player_pov = undefined
let tick_timeout = 500

function create_empty_map() {
    DRAW = SVG().addTo('body').size('100%', '100%')
    DRAW_HEX_GROUP = DRAW.group()
    TEXT_GROUP = DRAW.group()
    // HIDE_HEXAGON_GROUP = DRAW.group()

    const corners = Hex().corners()
    const hexSymbol = DRAW.symbol()
        .polygon(corners.map(({ x, y }) => `${x},${y}`))
        .stroke({ width: 4, color: '#999' })

    for (let q = -SIDE; q <= SIDE; q++) {
        for (let r = -SIDE; r <= SIDE; r++) {
            const s = -(q + r)
            if (-SIDE <= s && s <= SIDE) {
                const hex = Hex({ q, r, s })
                const { x, y } = hex.toPoint()
                let hexagon = DRAW_HEX_GROUP.use(hexSymbol).translate(x, y)
                hexagon.fill('none')

                hexagon_map[[q, r, s]] = hexagon

                const { cx, cy } = hexagon.rbox()
                const p = DRAW.point(cx, cy)
                let t = TEXT_GROUP.text('').font({ size: 40 }).center(p.x, p.y)
                text_labels[[q, r, s]] = t

                // let hide_hexagon = HIDE_HEXAGON_GROUP.use(hexSymbol).translate(x, y).fill('red').hide()
                // hide_hexagon_map[[q, r, s]] = hide_hexagon
            }
        }
    }
    DRAW.viewbox(DRAW_HEX_GROUP.bbox())
}

async function load_empty_map() {
    const svg = await fetch('/empty_map.svg').then(r => r.text())
    DRAW = SVG(svg).addTo('body').size('100%', '100%')
    DRAW_HEX_GROUP = DRAW.children()[0]
    TEXT_GROUP = DRAW.children()[1]
    // HIDE_HEXAGON_GROUP = DRAW.children()[2]

    const all_empty_hexagons = DRAW_HEX_GROUP.children()
    const all_empty_labels = TEXT_GROUP.children()
    // const all_hide_hexagons = HIDE_HEXAGON_GROUP.children()

    for (let q = -SIDE; q <= SIDE; q++) {
        for (let r = -SIDE; r <= SIDE; r++) {
            const s = -(q + r)
            if (-SIDE <= s && s <= SIDE) {
                let hexagon = all_empty_hexagons.shift()
                hexagon_map[[q, r, s]] = hexagon

                let label = all_empty_labels.shift()
                text_labels[[q, r, s]] = label

                // let hide_hexagon = all_hide_hexagons.shift()
                // hide_hexagon_map[[q, r, s]] = hide_hexagon
            }
        }
    }
    DRAW.viewbox(DRAW_HEX_GROUP.bbox())
}

async function edit_hexagon(hex) {

    const q = hex.q
    const r = hex.r
    const s = hex.s
    const point_type = hex.point_type
    const owner_ID = hex.owner_ID
    const current_value = hex.current_value

    let text = undefined
    let color = 'none'

    if (point_type === POINT_TYPES.FLAG) {
        text = `S ${current_value}`
        color = PLAYER_COLORS[owner_ID]
    } else if (point_type === POINT_TYPES.GRASS) {
        if (current_value !== 0) {
            text = `${current_value}`
        }
        color = PLAYER_COLORS[owner_ID]
    } else if (point_type === POINT_TYPES.WALL) {
        color = 'black'
    } else if (point_type === POINT_TYPES.FORT) {
        text = `H ${current_value}`
        color = PLAYER_COLORS[owner_ID]
    } else if (point_type === POINT_TYPES.CRYPTO_CRYSTAL) {
        text = `CC ${current_value}`
        color = 'green'
    } else if (point_type === POINT_TYPES.WEB_CRYSTAL) {
        text = `WC ${current_value}`
        color = 'yellow'
    } else if (point_type === POINT_TYPES.REV_CRYSTAL) {
        text = `RC ${current_value}`
        color = 'blue'
    } else if (point_type === POINT_TYPES.PWN_CRYSTAL) {
        text = `PC ${current_value}`
        color = 'purple'
    } else if (point_type === POINT_TYPES.MISC_CRYSTAL) {
        text = `MC ${current_value}`
        color = 'brown'
    } else if (point_type === POINT_TYPES.UNKNOWN_EMPTY) {
        color = 'grey'
    } else if (point_type === POINT_TYPES.UNKNOWN_OBJECT) {
        color = 'purple'
    }

    // const hide_hexagon = hide_hexagon_map[[hex.q, hex.r, hex.s]]
    if (player_pov !== undefined) {
        if (
            owner_ID !== player_pov &&
            !(
                hex_map[[q + 1, r - 1, s]]?.owner_ID === player_pov ||
                hex_map[[q - 1, r + 1, s]]?.owner_ID === player_pov ||
                hex_map[[q + 1, r, s - 1]]?.owner_ID === player_pov ||
                hex_map[[q - 1, r, s + 1]]?.owner_ID === player_pov ||
                hex_map[[q, r + 1, s - 1]]?.owner_ID === player_pov ||
                hex_map[[q, r - 1, s + 1]]?.owner_ID === player_pov
            )
        ) {
            // hide_hexagon.show()
            text = undefined
            if (point_type === POINT_TYPES.GRASS || point_type === POINT_TYPES.FLAG) {
                color = 'grey'
            } else {
                color = 'purple'
            }
        } else {
            // hide_hexagon.hide()
        }
    } else {
        // hide_hexagon.hide()
    }


    const hexagon = hexagon_map[[hex.q, hex.r, hex.s]]

    if (hexagon.fill() !== color) {
        hexagon.fill(color)
    }


    if (text) {
        const label = text_labels[[hex.q, hex.r, hex.s]]
        const { cx, cy } = hexagon.rbox()
        const p = DRAW.point(cx, cy)
        if (label) {
            label.show()
            if (label.text() !== text) {
                label.text(text).center(p.x, p.y)
            }
        } else {
            let t = TEXT_GROUP.text(text).font({ size: 40 }).center(p.x, p.y)
            text_labels[[hex.q, hex.r, hex.s]] = t
        }
    } else {
        const label = text_labels[[hex.q, hex.r, hex.s]]
        if (label) {
            label.hide()
        }
    }
}

async function get_history() {
    return await fetch('/history.json').then(r => r.json())
}

function add_info_to_map(data) {
    // let to_edit_hex = []
    for (const p of data) {
        const [q, r, s] = p[0]
        const point_type = p[1]
        const owner_ID = p[2]
        const current_value = p[3]

        const hex = Hex({ q, r, s, point_type, owner_ID, current_value })

        hex_map[[q, r, s]] = hex
        // to_edit_hex.push(hex)
    }

    for (const hex of Object.values(hex_map)) {
        edit_hexagon(hex)
    }
}

function update_stats() {
    stats = {}

    for (const hex of Object.values(hex_map)) {
        if (hex.current_value !== 0 && hex.owner_ID !== null) {
            if (!stats[hex.owner_ID]) {
                stats[hex.owner_ID] = {
                    troops: hex.current_value,
                    terr: 1
                }
            } else {
                stats[hex.owner_ID].troops += hex.current_value
                stats[hex.owner_ID].terr += 1
            }
        }
    }

    for (const t of players) {
        troop_element = document.getElementById('troops-' + t)
        terr_element = document.getElementById('terr-' + t)
        if (stats[t] === undefined) {
            // dead
            troop_element.innerText = '-'
            terr_element.innerText = '-'
        } else {
            troop_element.innerText = stats[t].troops
            terr_element.innerText = stats[t].terr
        }
    }

}

function enable_buttons() {
    for (const button of document.getElementsByTagName('button')) {
        button.disabled = false
    }
}

async function start() {

    // create_empty_map()
    await load_empty_map()

    DRAW.panZoom({
        zoomFactor: 0.2,
        zoomMin: 0.1,
        zoomMax: 10,
    })


    // load data and draw tick 0
    let map_history = await get_history()
    tick = 0
    add_info_to_map(map_history[tick])


    function next_tick() {
        if (tick < (map_history.length - 1)) {
            tick++
            add_info_to_map(map_history[tick])
            update_stats()
            // console.log(`tick ${tick}`)
            document.getElementById('ticknumber').innerText = tick
        }
    }

    document.getElementById('tick').addEventListener('click', e => {
        next_tick()
    })

    let intervalid = undefined

    function start_ticking() {
        if (intervalid === undefined) {
            intervalid = setInterval(() => {
                if (tick >= map_history.length) {
                    clearInterval(intervalid)
                } else {
                    next_tick()
                }
            }, tick_timeout)
        }
    }

    function stop_ticking() {
        if (intervalid !== undefined) {
            clearInterval(intervalid)
            intervalid = undefined
        }
    }

    document.getElementById('start').addEventListener('click', e => {
        start_ticking()
    })

    document.getElementById('stop').addEventListener('click', e => {
        stop_ticking()
    })

    document.getElementById('restart').addEventListener('click', e => {
        stop_ticking()
        tick = -1
        next_tick()
    })

    const pov_select = document.getElementById('pov')
    const stats_div = document.getElementById('stats')

    for (const t of players) {
        // select pow
        let opt = document.createElement('option', { value: t })
        opt.textContent = t
        pov_select.appendChild(opt)

        // initialize stats
        let row = document.createElement('tr')
        let el = document.createElement('td')
        el.textContent = t
        row.appendChild(el)
        el = document.createElement('td')
        el.textContent = '1'
        el.id = 'troops-' + t
        row.appendChild(el)
        el = document.createElement('td')
        el.textContent = '1'
        el.id = 'terr-' + t
        row.appendChild(el)
        stats_div.appendChild(row)
    }

    document.getElementById('pov').addEventListener('change', e => {
        let s = parseInt(e.target.selectedOptions[0].value)
        if (s === -1) {
            s = undefined
        }
        player_pov = s
        add_info_to_map(map_history[tick])
    })

    document.getElementById('speed').addEventListener('change', e => {
        const speed = e.target.value
        tick_timeout = Math.floor((10000 / speed))
        console.log(tick_timeout)
        if (intervalid !== undefined) {
            stop_ticking()
            start_ticking()
        }
    })

    document.getElementById('speed').value = Math.floor(10000 / tick_timeout)


    enable_buttons()
}


// create_empty_map()
start()
