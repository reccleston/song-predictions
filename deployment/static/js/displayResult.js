window.onload = (event) => {
    hitDiv = d3.select('#hitDiv');
    hitText = hitDiv.select('#hitAlert').node().textContent;
    if (hitText == 'Your song choice is likely to be a hit!') {
        console.log('its a hit')
        hitDiv.classed('invisible', false)
        hitDiv.classed('alert-success', true)
        hitDiv.classed('alert-danger', false)
    //   hitDiv.style('visibility', 'visible');
    //   hitDiv.classed('alert-success', true);
    } else if (hitText == 'Your song choice is likely to not be a hit!') {
        console.log('not a hit')
        hitDiv.classed('invisible', false)
        hitDiv.classed('alert-success', false)
        hitDiv.classed('alert-danger', true)
    //   hitDiv.style('visibility', 'visible');
    //   hitDiv.classed('alert-error', true);
    } else {
        console.log('no song is chosen yet')
        hitDiv.classed('invisible', true)
    } ;
};