const SIDE = 50

const DRAW = SVG().addTo('body').size('100%', '100%')
const DRAW_HEX_GROUP = DRAW.group()
const TEXT_GROUP = DRAW.group()

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


let hexagon_map = {}
let hex_map = {}
let text_labels = {}
let player_pov = 0


function create_empty_map() {
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
            }
        }
    }
    DRAW.viewbox(DRAW_HEX_GROUP.bbox())
}

function edit_hexagon(hex) {

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
        text = `${current_value}`
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

    if (player_pov) {
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
            text = undefined
            if (point_type === POINT_TYPES.GRASS || point_type === POINT_TYPES.FLAG) {
                color = 'grey'
            } else {
                color = 'purple'
            }
        }
    }


    const hexagon = hexagon_map[[hex.q, hex.r, hex.s]]

    hexagon.fill(color)

    if (text) {
        const label = text_labels[[hex.q, hex.r, hex.s]]
        if (label) {
            label.text(text)
        } else {
            const { cx, cy } = hexagon.rbox()
            const p = DRAW.point(cx, cy)
            let t = TEXT_GROUP.text(text).font({ size: 40 }).center(p.x, p.y);

            text_labels[[hex.q, hex.r, hex.s]] = t
        }
    }
}


async function get_history() {
    return await fetch('/history.json').then(r => r.json())
}


function add_info_to_map(data) {
    // let data = JSON.parse(json_dump)
    let to_edit_hex = []
    for (const p of data) {
        const [q, r, s] = p[0]
        const point_type = p[1]
        const owner_ID = p[2]
        const current_value = p[3]

        const hex = Hex({ q, r, s, point_type, owner_ID, current_value })

        hex_map[[q, r, s]] = hex
        to_edit_hex.push(hex)
    }

    for (const hex of Object.values(hex_map)) {
        edit_hexagon(hex)
    }
}


create_empty_map()

DRAW.panZoom({
    zoomFactor: 0.2,
    zoomMin: 0.1,
    zoomMax: 10,
})

function enable_buttons() {
    for (const button of document.getElementsByTagName('button')) {
        button.disabled = false
    }
}

async function start() {

    // load data and draw tick 0
    let map_history = await get_history()
    add_info_to_map(map_history[0])
    tick = 1


    function next_tick() {
        console.log(`tick ${tick}`)
        add_info_to_map(map_history[tick])
        tick++
    }

    document.getElementById('tick').addEventListener('click', e => {
        next_tick()
    })

    let intervalid = undefined

    document.getElementById('start').addEventListener('click', e => {
        if (intervalid === undefined) {
            intervalid = setInterval(() => {
                if (tick >= map_history.length) {
                    clearInterval(intervalid)
                } else {
                    next_tick()
                }
            }, 500)
        }
    })

    document.getElementById('stop').addEventListener('click', e => {
        if (intervalid !== undefined) {
            clearInterval(intervalid)
            intervalid = undefined
        }
    })

    document.getElementById('pov').addEventListener('click', e => {
        player_pov=parseInt(document.getElementById('player').value);
        create_empty_map();
        start()
    })



    enable_buttons()
}

start()