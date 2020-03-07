import { Image } from './../image.component';
import { Component, OnInit, Input, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { VmService } from '@app/services/vm.service';
// import { isDefined } from '@angular/compiler/src/util';

export interface ImageDeploy{
  instance_name: string,
  flavor: string,
  root_password: string
}

@Component({
  selector: 'app-image-item',
  templateUrl: './image-item.component.html',
  styleUrls: ['./image-item.component.css']
})
export class ImageItemComponent implements OnInit {
  @Input() image: Image;
  imageDeploy: ImageDeploy;
  deletable: boolean;
  

  constructor(
    private vmService: VmService,
    public dialog: MatDialog
  ) { }

  ngOnInit() {
    if(JSON.parse(localStorage.getItem('currentUser'))["username"] == this.image.username){
      this.deletable = true;
    }
    else{
      this.deletable = false;
    }
  }

  openImageDialog(): void {
    const dialogRef = this.dialog.open(DialogImageDeploy, {
      width: '250px',
      data: {instance_name: "", flavor: "", root_password: ""}
    });

    dialogRef.afterClosed().subscribe(result => {
      this.imageDeploy = result;
      if(this.imageDeploy.instance_name != "" &&
      this.imageDeploy.flavor != "" &&
      this.imageDeploy.root_password != ""){
        this.vmService.deployInstance(
          this.imageDeploy.instance_name, 
          this.imageDeploy.root_password,
          this.image.name,
          this.imageDeploy.flavor)
        .subscribe(data=>{
          alert("Successful Deployed");
        },
        error=>alert("Failed"))
      }
    });
  }
}

@Component({
  selector: 'dialog-image-deploy',
  templateUrl: 'image-deploy.html'
})
export class DialogImageDeploy{
  flavors = ["small", "medium", "large"];

  constructor(
    public dialogRef: MatDialogRef<DialogImageDeploy>,
    @Inject(MAT_DIALOG_DATA) public data: ImageDeploy) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}