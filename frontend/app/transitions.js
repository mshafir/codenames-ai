export default function(){
	this.transition(
    this.hasClass('fade'),
    this.use('fade')
  );

	this.transition(
    this.hasClass('flipX'),
    this.use('flipX')
  );

  this.transition(
    this.hasClass('flipY'),
    this.use('flipY')
  );
}
