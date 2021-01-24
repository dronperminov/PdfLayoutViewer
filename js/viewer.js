function LayoutViewer(blocks) {
    this.blocks = blocks
}

LayoutViewer.prototype.RemoveBlocks = function() {
    for (let i = 0; i < this.blocks.length; i++) {
        let block = document.getElementById(`img-${i}`)
        
        if (block.children.length > 1)
            block.removeChild(block.lastChild)
    }
}

LayoutViewer.prototype.MakeBlock = function(block, width, height) {
    let w = Math.abs(block.x2 - block.x1)
    let h = Math.abs(block.y2 - block.y1)

    let box = document.createElement('div')
    
    box.innerHTML = ''
    box.style.position = 'absolute'
    box.style.width = (w * 100 * width) + '%'
    box.style.height = (h * 100 * height) + '%'
    box.style.left = (block.x1 * 100 * width) + '%'
    box.style.top = (block.y1 * 100 * height) + '%'
    box.style.background = 'rgba(255, 0, 0, 0.5)'

    return box
}

LayoutViewer.prototype.ScrollTo = function(page_id, block_id) {
    this.RemoveBlocks()    

    let block = blocks[page_id][block_id]
    let img = document.getElementById(`img-${page_id}`)

    let width = img.firstChild.offsetWidth / img.offsetWidth
    let height = img.firstChild.offsetHeight / img.offsetHeight

    let box = this.MakeBlock(block, width, height)

    img.appendChild(box)
    box.scrollIntoView({block: "center", behavior: "smooth"});
}