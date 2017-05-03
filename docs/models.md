# Django Models 

This file drafts the database models to be used in the Django News platform,
including everything from users to reports to media.

## Model List

### New Model


## Old Model List

These models are scraped off of the existing SQL files in the respective 
directory of the current Silver Chips Online deploy. Unfortunately, this was 
done by hand.

### Award

**Name**: `award` <br>
**Fields**: `date: datetime`, `text: %s`

The usage of this database model is unclear, but is most likely to store student
awards for academic or extracurricular achievement. 

### Chips Shot

**Name** `chips_shot` <br>
**Fields**: `date: datetime`, `pid: %d`

This model could have been used to store images or some other variety of indexed
resource.

### Comment

**Name**: `comment` <br>
**Fields**: `tid: %d`, `pid: %d`, `uname: %s`, `author_name: %s`, 
`author_email: %s`, `date: datetime`, `status: %s`, `ip: %s`, `text: %s`

Most likely used to store user comments on stories and reports. Field `tid` and
`pid` are unclear in use, but are common in occurrence. 

### Comment Thread

**Name**: `comment_thread` <br>
**Fields**: `none`

Unclear if ever actually used.

### Section Content

**Name**: `section_content` <br>
**Fields**: `sectionId: %d`, `contentId: %d`, `type: %s`

Possibly used for dynamically loading HTML or report contents.

### Cycle Folder Draft

**Name**: `cycleFolder_draft` <br>
**Fields**: `folderId: %d`, `editorId: %d`, `editType: %s`

Might have been used for maintaining stories before publishing.

### Cycle Folder

**Name**: `cycleFolder` <br>
**Fields**: `userId: %d`, `cycleId: 1`, `storyId: %d`, `name: %s`

### Event

**Name**: `event` <br>
**Fields**: `date: datetime`, `author: %s`, `name: %s`, `email: %s`, 
`typeId: %d`, `description: %s`, `status: %s`, `featured: %d`, `blair: %d`,
`location: %s`, `pid: %d`, `sid: %d`, `metro: %d`

Could have been used to store calendar events or report locations.

### Featured Quote

**Name**: `feature_quote` <br>
**Fields**: `quote: %s`

Possibly for some external quote reference.

### Gallery Picture

**Name**: `gallery_picture` <br>
**Fields**: `gid: %d`, `pid: %d`

Most likely used to store digital pictures for reference in a gallery.

### Gallery

**Name**: `gallery` <br>
**Fields**: `name: %s`, `description: %s`, `isSlideshow: %d`, 
`commentThreadId: %d`

Tracks a name, description, display mode, and comment thread, but no pictures?

### Job

**Name**: `job` <br>
**Fields**: `type: %s`, `date: datetime`, `title: %s`, `location: %s`, 
`hours: %s`, `qualifications: %s`, `contact: %s`, `phone: %s`, `description: %s`

Maintains employment information. Why does anyone need this?

### Picture

**Name**: `picture` <br>
**Fields**: `date: datetime`, `authorId: %d`, `altAuthor: %s`, `title: %s`,
`goodTitle: %s`, `caption: %s`, `picType: %s`, `mimeType: %s`, `width: %d`,
`height: %d`, `thumb_x: %d`, `thumb_size: %d`, `commentThreadId: %d`

This is what keeps database engineers up at night. 

### Poll IP

**Name**: `poll_ip` <br>
**Fields**: `pid: %d`, `ip: %d`, `seen: datetime`

This is probably for checking who submits responses to polls.

### Poll Option

**Name**: `poll_option` <br>
**Fields**: `pid: %d`, `id: %d`, `option: %s`, `votes: %d`

Poll options were their own container.

### Add Poll

**Name**: `add_poll` <br>
**Fields**: `question: %s`, `locked: %s`, `commentThreadId: %d`

Not sure how a method managed to transform into a SQL item.

### Print Edition

**Name**: `printedition` <br>
**Fields**: `issue: %s`

Some sort of container for print copy reference.

### Quote

**Name**: `quote` <br>
**Fields**: `quote: %s`

A quote container.

### Rating IP

**Name**: `rating_ip` <br>
**Fields**: `rating: %d`, `ip: %d`, `seen: datetime`

A model for preventing multiple submissions of ratings.

### Rating

**Name**: `rating` <br>
**Fields**: `value: %f`, `votes: %d`

Model for storing a rating and number of votes.

### Role Action

**Name**: `role_action` <br>
**Fields**: `id: %d`, `actionId: %d`

Could have been used to denote actions of a role.

### Role

**Name**: `role` <br>
**Fields**: `name: %s`

Stores some sort of job that has actions. 

### Speak Out

**Name**: `speakout` <br>
**Fields**: `question: %s`, `commentThreadId: %d`

Container for starting revolutions.

### Sports Event

**Name**: `sports_event` <br>
**Fields**: `date: datetime`, `sport: %s`, `level: %s`, `location: %s`, 
`opponent: %s`, `ourscore: %d`, `theirscore: %d`, `result: %s`, `storyId: %d`

Used for tracking school sports events. 

### Story Author

**Name**: `story_author` <br>
**Fields**: `sid: %d`, `uid: %d`

Used to track the author of a story.

### Story Relation

**Name**: `story_relation` <br>
**Fields**: `id: %d`, `relatedId: %d`

Maybe used to keep track of related content to an article.

### Story

**Name**: `story` <br>
**Fields**: `cid: %d`, `headline: %s`, `secdeck: %s`, `date: datetime`,
`terminate: %s`, `lead: %s`, `text: %s`, `published: %s`, `rewrite: %s`,
`commentThreadId: %d`, `mainMediaId: %d`

What kind of evil must a person be to do this?

### Story Tag

**Name**: `story_tag` <br>
**Fields**: `sid: %d`, `name: %s`

Individual story tags.

### User Role

**Name**: `user_role` <br>
**Fields**: `id: %d`, `roleId: %d`

Used to track what a user can do?

### User

**Name**: `user` <br>
**Fields**: `uname: %s`, `fname: %s`, `lname: %s`, `editor: %d`, `email: %s`,
`gradyear: %d`, `bio: %s`, `position: %s`, `active: %s`, `pid: %d`

Used to track information of individual users.

### Weekend

**Name**: `weekend` <br>
**Fields**: `title: %s`, `pid: %d`, `type: %s`, `date: datetime`, `blurb: %s`,
`metro: %d`, `sid: %d`

Not entirely sure why it is necessary to have a weekend in the database.
