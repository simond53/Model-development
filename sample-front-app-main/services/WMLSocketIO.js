

const {processdata} = require('./WMLClient');
const {modelDeploymentUrl} = require('../config/WMLService')
let io;

module.exports = function (app) {

    io = require('socket.io')(app);

    
io.on( 'connection', function( socket )
{
	console.log( 'io: connection...' );

	socket.on( 'sendtomodel', function( data )
	{
		console.log( 'io: sendtomodel...' ); 

        processdata( modelDeploymentUrl, data ).then( function( result )
        {
            console.log( "Result:\n" + JSON.stringify( result, null, 3 ) );
            socket.emit( 'processresult', result );

        } ).catch( function( error )
        {
            console.log( "Error:\n" + error );
            socket.emit( 'processresult', { "error" : error } );

        } );

	} );
} );
};