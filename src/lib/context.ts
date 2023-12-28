import { setInLocalStorage } from "./scrollStore"

interface MainContext {
    getGripPosition(): number
    // Move the grip position by n (n in [0, 1])
    updateGridPosition(n: number) 
    setGridPosition(n: number)
    // Total number of messages
    getTotalMessages(): number
    getVisibleMessages(): Message[]
    getFirstVisibleMessage(): Message
}

interface Message {
    text: string
    id: number
}

function updateGridPosition(n: number) {
    let current = getGripPosition()
    setGridPosition(current + n)
}

function setGridPosition(n: number) {
    setInLocalStorage('gripPosition', n)
}

function getGripPosition(): number {
    return localStorage.getItem("gripPosition")
}

<script>
    let { updateGridPosition, getGridPosition, getVisibleMessages } = load() // Loading the MainContext
</script>